from bs4 import BeautifulSoup, NavigableString, Tag
from ..utils import logger
from ..translate.html2json_base import Html2JsonBase, Block
from ..utils.timeutil import DateStrToISO8601

YinXiangClipper_Type = "clipper.yinxiang"


class Html2JsonYinXiang(Html2JsonBase):
    input_type = YinXiangClipper_Type

    def __init__(self, html_content):
        super().__init__(html_content)

    def process(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        self.convert_properties(soup)

        content_tags = soup.body
        if not content_tags:
            logger.warning("No content found")
            return
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
        elif tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            return Block.HEADING.value
        elif tag_name == 'hr':
            return Block.DIVIDER.value
        elif tag_name == 'ol':
            return Block.NUMBERED_LIST.value
        elif tag_name == 'ul':
            return Block.BULLETED_LIST.value
        elif tag_name == 'p':
            return Block.PARAGRAPH.value
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
            else:
                logger.warning(f"Unknown cnvert {element}, {block_type}")
        return

Html2JsonBase.register(YinXiangClipper_Type, Html2JsonYinXiang)
