from bs4 import BeautifulSoup, Tag
from ..utils import logger, DateStrToISO8601
from ..translate.html2json_base import Html2JsonBase, Block 

YinXiang_Type = "yinxiang"


class Html2JsonYinXiang(Html2JsonBase):
    input_type = YinXiang_Type

    def __init__(self, html_content, import_stat):
        super().__init__(html_content, import_stat)

    def process(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        self.convert_children(soup)
        self.convert_properties(soup)
        return YinXiang_Type

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

    def convert_children(self, soup):
        content_tags = soup.find_all('body', recursive=True)
        if not content_tags:
            logger.warning("No content found")
            raise Exception("No content found")

        self.import_stat.add_text(content_tags[0].get_text())
        for child in content_tags[0].children:
            block_type = self.get_block_type(child)
            # Computer all text len in html
            logger.debug(f'Support tag {child} with style {block_type}')
            if hasattr(self, f"convert_{block_type}"):
                converter = getattr(self, f"convert_{block_type}")
                block = converter(child)
                if block:
                    self.children.extend([block] if not isinstance(block, list) else block)
            else:
                self.import_stat.add_skip_tag(child.get_text())
                logger.warning(f"Unknown tag : {child}")
    
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

        children_list = list(soup.children) if isinstance(soup, Tag) else [soup]
        for index, child in enumerate(children_list):
            is_last_child = index == len(children_list) - 1
            text_obj = self.generate_inline_obj(child)
            if text_obj:
                rich_text.extend(text_obj)
            if not is_last_child:
                rich_text.append(self.generate_text(plain_text='\n', stats_count=False))
        json_obj["code"]["rich_text"] = self.merge_rich_text(rich_text)
        css_dict = Html2JsonBase.get_tag_style(soup)
        language = css_dict.get('--en-codeblockLanguage', 'plain text')
        json_obj["code"]["language"] = language
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

        children_list = list(soup.children)
        for index, child in enumerate(children_list):
            is_last_child = index == len(children_list) - 1
            text_obj = self.generate_inline_obj(child)
            if text_obj:
                rich_text.extend(text_obj)
            if not is_last_child:
                rich_text.append(self.generate_text(plain_text='\n', stats_count=False))

        # Merge tags has same anotions
        logger.debug(f'before merge: {rich_text}')
        json_obj["quote"]["rich_text"] = self.merge_rich_text(rich_text)
        return json_obj

    def convert_to_do(self, soup: Tag):
        # Compatible with the situation where input is under li tag(super note).
        li_tags = soup.find_all('li', recursive=True)
        childs = li_tags if li_tags else [soup]
        to_do_blocks = []
        for child in childs:
            json_obj = {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [],
                    "checked": False
                }
            }
            text = json_obj["to_do"]["rich_text"]
            text_obj = self.generate_inline_obj(child)
            if text_obj:
                text.extend(text_obj)
            input_tag = child.find('input')
            if input_tag and isinstance(input_tag, Tag) and input_tag.get('checked', 'false') == 'true':
                json_obj["to_do"]["checked"] = True
            to_do_blocks.append(json_obj)
        return to_do_blocks
  
    def get_block_type(self, single_tag):
        tag_name = single_tag.name
        style = single_tag.get('style') if tag_name else ""

        # There are priorities here. It is possible to hit multiple targets 
        # at the same time, and the first one takes precedence.
        if self._check_is_todo(single_tag):
            return Block.TO_DO.value
        elif tag_name == 'hr':
            return Block.DIVIDER.value
        elif tag_name == 'ol':
            return Block.NUMBERED_LIST.value
        elif tag_name == 'ul':
            return Block.BULLETED_LIST.value
        elif tag_name == 'p':
            return Block.PARAGRAPH.value
        elif tag_name in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            return Block.HEADING.value
        elif tag_name == 'table' or self._check_is_table(single_tag):
            return Block.TABLE.value
        
        css_dict = Html2JsonBase.get_tag_style(single_tag)
        if css_dict.get('--en-blockquote', None) == 'true':
            return Block.QUOTE.value
        if css_dict.get('--en-codeblock', None) == 'true':
            return Block.CODE.value
        if css_dict.get('-en-codeblock', None) == 'true':
            return Block.CODE.value

        # Issue 5: <div style="orphans: 2; widows: 2">
        if tag_name == 'div':
            return Block.PARAGRAPH.value
        return Block.FAIL.value

    # <div> <table> </table> </div>
    def _check_is_table(self, tag):
        if tag.name == "div":
            children = list(filter(lambda x: x != '\n', tag.contents))
            table_count = sum(1 for child in children if child.name == "table")
            return table_count >= 1
        return False

    def _check_is_todo(self, tag):
        if not isinstance(tag, Tag):
            return False
        input_tag = tag.find('input')
        if input_tag and isinstance(input_tag, Tag) and input_tag.get('type') == 'checkbox':
            return True
        return False

Html2JsonBase.register(YinXiang_Type, Html2JsonYinXiang)
