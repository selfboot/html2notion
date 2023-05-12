import re
from bs4 import BeautifulSoup, Tag
from urllib.parse import unquote
from ..utils import logger
from ..translate.html2json_base import Html2JsonBase, Block
from ..utils.timeutil import DateStrToISO8601

YinXiangMarkdown_Type = "markdown.yinxiang"

# Yinxiang markdown
# https://list.yinxiang.com/markdown/eef42447-db3f-48ee-827b-1bb34c03eb83.php


class Html2JsonMarkdown(Html2JsonBase):
    input_type = YinXiangMarkdown_Type
    undo_image = "url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAAAXNSR0IArs4c6QAAADdJREFUKBVjvHv37n8GMgALSI+SkhJJWu/du8fARJIOJMWjGpECA505GjjoIYLEB6dVUNojFQAA/1MJUFWet/4AAAAASUVORK5CYII=')"

    def __init__(self, html_content, import_stat):
        super().__init__(html_content, import_stat)
        self.markdown = ""

    def process(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        self.convert_properties(soup)

        content_tags = soup.body
        if not content_tags:
            logger.error("No content found")
            raise Exception("No content found")

        # The center records the contents of the original markdown file, which is useless
        center_to_delete = content_tags.find('center')
        if isinstance(center_to_delete, Tag):
            md_encode = center_to_delete.get_text()
            self.markdown = unquote(md_encode)
        if isinstance(center_to_delete, Tag):
            center_to_delete.decompose()

        # Special handling contains blocks of code, 
        # because some chart blocks are converted into images and cannot be processed directly
        self._replace_pre_code(soup)
        self.import_stat.add_text(content_tags.get_text())
        self.convert_children(content_tags)  # Assesume only one body tag

        return YinXiangMarkdown_Type

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
            if self._is_checkbox(element):
                return Block.TO_DO.value
            return Block.BULLETED_LIST.value
        elif element.name == 'pre' and element.code:
            if self._is_math(element):
                return Block.EQUATION.value
            return Block.CODE.value
        elif element.name == "blockquote":
            return Block.QUOTE.value

        return Block.FAIL.value

    def convert_children(self, soup):
        div_tag = soup.find('div')
        if not div_tag:
            logger.error(f'No div tag found in {soup}')
            return
        for child in div_tag.children:
            block_type = self.get_block_type(child)
            logger.debug(f'block_type: {block_type}, child: {child}')
            if hasattr(self, f"convert_{block_type}"):
                converter = getattr(self, f"convert_{block_type}")
                block = converter(child)
                if block:
                    self.children.extend([block] if not isinstance(block, list) else block)
            else:
                self.import_stat.add_skip_tag(child.get_text())
                logger.warning(f"Unknown tag : {child}")
        return

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
            text_obj = self.generate_inline_obj(child)
            if text_obj:
                rich_text.extend(text_obj)

        css_dict = Html2JsonBase.get_tag_style(code_tag)
        language = css_dict.get('language', 'plain text')
        json_obj["code"]["language"] = language
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
        return json_obj

    def convert_to_do(self, soup: Tag):
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

            style = child.get('style', '')
            if isinstance(style, str) and Html2JsonMarkdown.undo_image not in style:
                json_obj["to_do"]["checked"] = True
            to_do_blocks.append(json_obj)
        return to_do_blocks

    # Each style in <li> has a background-image, which is considered a check box
    def _is_checkbox(self, soup):
        for li in soup.find_all('li'):
            style = li.get('style', '')
            if not "background-image: url('data:image/png;" in style:
                return False
        return True

    def _extract_code_blocks(self):
        code_pattern = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)
        matches = code_pattern.findall(self.markdown)
        code_blocks = [{'language': Html2JsonBase.get_valid_language(match[0]), 'code': match[1]} for match in matches]
        return code_blocks

    def _replace_pre_code(self, soup):
        markdown_code_blocks = self._extract_code_blocks()
        count = sum(1 for pre_tag in soup.find_all('pre') if pre_tag.find('code'))

        if markdown_code_blocks and count != len(markdown_code_blocks):
            logger.warning(f'Code block count not match: {count} != {len(markdown_code_blocks)}')
            return

        pre_tags = soup.find_all('pre')
        idx = 0
        for pre in pre_tags:
            code = pre.find('code')
            if not code:
                continue
            new_tag = soup.new_tag('code')
            new_tag.string = markdown_code_blocks[idx]['code']
            new_tag['style'] = 'language: ' + markdown_code_blocks[idx]['language']
            idx += 1
            code.replace_with(new_tag)
        return soup

    def _is_math(self, soup):
        code_tag = soup.code
        if not code_tag:
            return False

        css_dict = Html2JsonBase.get_tag_style(code_tag)
        if 'language' in css_dict and css_dict['language'] == 'math':
            return True
        return False


Html2JsonBase.register(YinXiangMarkdown_Type, Html2JsonMarkdown)
