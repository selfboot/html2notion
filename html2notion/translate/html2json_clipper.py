from bs4 import BeautifulSoup, NavigableString, Tag
from ..utils import logger
from ..translate.html2json_base import Html2JsonBase, Block
from ..utils.timeutil import DateStrToISO8601

YinXiangClipper_Type = "clipper.yinxiang"


class Html2JsonClipper(Html2JsonBase):
    input_type = YinXiangClipper_Type

    def __init__(self, html_content, import_stat):
        super().__init__(html_content, import_stat)

    def process(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        self.convert_properties(soup)

        content_tags = soup.body
        if not content_tags:
            logger.error("No content found")
            raise Exception("No content found")

        self.import_stat.add_text(content_tags.get_text())
        self.convert_children(content_tags)  # Assesume only one body tag

        return YinXiangClipper_Type

    def convert_properties(self, soup):
        properties = {"title": "Unknown"}
        title_tag = soup.select_one('head > title')
        if title_tag:
            properties["title"] = title_tag.text

        meta_tags = [
            ('head > meta[name="source-url"]', "url"),
            ('head > meta[name="keywords"]', "tags", lambda x: x.split(",")),
            ('head > meta[name="created"]', "created_time", DateStrToISO8601),
        ]

        for selector, key, *converter in meta_tags:
            tag = soup.select_one(selector)
            if tag and tag.get('content', None):
                content = tag['content']
                properties[key] = converter[0](content) if converter else content

        self.properties = self.generate_properties(**properties)
        return

    def get_block_type(self, element):
        tag_name = element.name
        if tag_name == "p":
            return Block.PARAGRAPH.value
        elif tag_name == "table":
            return Block.TABLE.value
        elif tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            return Block.HEADING.value
        elif tag_name == 'hr':
            return Block.DIVIDER.value
        elif tag_name == 'ol':
            return Block.NUMBERED_LIST.value
        elif tag_name == 'ul':
            return Block.BULLETED_LIST.value
        elif element.name == 'pre' and element.code:
            return Block.CODE.value
        elif self._check_is_block(element):
            return Block.QUOTE.value

        return Block.FAIL.value

    def convert_children(self, soup):
        processed_tags = set()
        for element in soup.descendants:
            if isinstance(element, NavigableString):
                continue
            if any(id(ancestor) in processed_tags for ancestor in element.parents):
                logger.debug(f"Skip processed tag {element}")
                continue
            block_type = self.get_block_type(element)
            if hasattr(self, f"convert_{block_type}"):
                converter = getattr(self, f"convert_{block_type}")
                block = converter(element)
                if block:
                    self.children.extend([block] if not isinstance(block, list) else block)
                    processed_tags.add(id(element))
        unprocessed_tags = set()
        for element in soup.descendants:
            if not isinstance(element, NavigableString) or id(element) in processed_tags:
                continue
            if any(id(ancestor) in processed_tags for ancestor in element.parents):
                continue
            unprocessed_tags.add(element)

        for unprocessed_tag in unprocessed_tags:
            logger.warning(f"Unknown tag {unprocessed_tag.name}, {self.get_block_type(unprocessed_tag)}")
            self.import_stat.add_skip_tag(unprocessed_tag.get_text())
        return

    # <pre><code><code>line number</code>... code content ...</code></pre>
    def convert_code(self, soup):
        json_obj = {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [],
                "language": "plain text",
            },
        }
        rich_text = json_obj["code"]["rich_text"]
        code_tag = soup.code
        if not code_tag:
            logger.error(f'No code tag found in {soup}')
            return
        children_list = list(code_tag.children) if isinstance(code_tag, Tag) else [code_tag]
        for child in children_list:
            if isinstance(child, Tag) and child.name == "code":
                logger.debug(f'Skip line number')
                continue
            text_obj = self.generate_inline_obj(child)
            if text_obj:
                rich_text.extend(text_obj)
        json_obj["code"]["rich_text"] = self.merge_rich_text(rich_text)
        return json_obj

    def convert_quote(self, soup):
        json_obj = {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": []
            }
        }
        rich_text = json_obj["quote"]["rich_text"]
        text_obj = self.generate_inline_obj(soup)
        if text_obj:
            rich_text.extend(text_obj)

        # Merge tags has same anotions
        return json_obj

    def _check_is_block(self, element):
        quote_elements = {'blockquote', 'q', 'cite'}
        if element.name in quote_elements:
            return True

        if element.name != 'div':
            return False

        # if 'class' in element.attrs:
        #     if any('quote' in class_name.lower() for class_name in element.attrs['class']):
        #         return True

        # if 'style' in element.attrs:
        #     style_attrs = element.attrs['style'].lower()
        #     if 'border:' in style_attrs or 'padding:' in style_attrs:
        #         return True

        return False

    
Html2JsonBase.register(YinXiangClipper_Type, Html2JsonClipper)
