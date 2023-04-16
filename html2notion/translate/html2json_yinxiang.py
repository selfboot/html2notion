from bs4 import BeautifulSoup, NavigableString
from ..utils import logger
from ..translate.html2json_base import Html2JsonBase, Block


YinXiang_Type = "yinxiang"


class Html2JsonYinXiang(Html2JsonBase):
    input_type = YinXiang_Type

    def __init__(self, html_content):
        super().__init__(html_content)

    def process(self):
        self.convert()
        return YinXiang_Type

    def convert(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        content_tags = soup.find_all('body', recursive=True)
        if not content_tags:
            logger.warning("No content found")
            return
        
        for child in content_tags[0].children:
            block_type = self.get_block_type(child)
            converter = getattr(self, f"convert_{block_type}")
            if converter:
                block = converter(child) 
                if block:
                    self.children.extend([block] if not isinstance(block, list) else block)
            else:
                logger.warning(f"Unknown block type: {block_type}")

    def convert_paragraph(self, soup):
        json_obj = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": []
            }
        }
        rich_text = json_obj["paragraph"]["rich_text"]
        for child in soup.children:
            tag_text = child.text if child.text else ""
            if not tag_text:
                continue
            text_obj = self.parse_inline_tag(child, tag_text)
            if text_obj:
                rich_text.append(text_obj)

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
        for child in soup.children:
            tag_text = child.text if child.text else ""
            if not tag_text:
                continue
            text_obj = self.parse_inline_tag(child, tag_text)
            if text_obj:
                rich_text.append(text_obj)

        # Merge tags has same anotions
        json_obj["quote"]["rich_text"] = self.merge_rich_text(rich_text)
        return json_obj

    # <ol><li><div>one</div></li><li><div>first</div></li><li><div>third</div></li></ol>
    def convert_numbered_list_item(self, soup):
        return self.convert_list_items(soup, 'numbered_list_item')

    # <ul><li><div>itemA</div></li><li><div>itemB</div></li><li><div>itemC</div></li></ul>
    def convert_bulleted_list_item(self, soup):
        return self.convert_list_items(soup, 'bulleted_list_item')

    def convert_list_items(self, soup, list_type):
        items = soup.find_all('li', recursive=True)
        if not items:
            logger.warning("No list items found in {soup}")

        json_arr = []
        for item in items:
            one_item = self._convert_one_list_item(item, list_type)
            if one_item:
                json_arr.append(one_item)
            else:
                logger.info(f'empty {item}')
        return json_arr

    def _convert_one_list_item(self, soup, list_type):
        if list_type not in {'numbered_list_item', 'bulleted_list_item'}:
            logger.warning(f'Not support list_type')

        json_obj = {
            "object": "block",
            list_type: {
                "rich_text": []
            },
            "type": list_type,
        }
        rich_text = json_obj[list_type]["rich_text"]
        for child in soup.children:
            tag_text = child.text if child.text else ""
            if not tag_text:
                continue
            text_obj = self.parse_inline_tag(child, tag_text)
            if text_obj:
                rich_text.append(text_obj)

        return json_obj


    # Todo Handle some recursive labels
    def _recursivr_inline_tag(self, tag_soup, tag_text, text_params):
        tag_name = tag_soup.name.lower() if tag_soup.name else ""
        style = tag_soup.get('style') if tag_name else ""
        styles = {}
        if style:
            styles = {rule.split(':')[0].strip(): rule.split(
                ':')[1].strip() for rule in style.split(';') if rule}

        text_params["plain_text"] = tag_text
        if Html2JsonBase.is_bold(tag_name, styles):
            text_params["bold"] = True
        if Html2JsonBase.is_italic(tag_name, styles):
            text_params["italic"] = True
        if Html2JsonBase.is_strikethrough(tag_name, styles):
            text_params["strikethrough"] = True
        if Html2JsonBase.is_underline(tag_name, styles):
            text_params["underline"] = True

        color = Html2JsonBase.get_color(
            styles, tag_soup.attrs if tag_name else {})
        if color != 'default':
            text_params["color"] = color

        if not tag_soup or isinstance(tag_soup, NavigableString):
            return

        for child in tag_soup.children:
            if child.name:
                self._recursivr_inline_tag(child, child.text, text_params)
        return
    
    # <b><u>下划线粗体</u></b>
    # <div><font color="#ff2600">红色4</font></div>
    def parse_inline_tag(self, tag_soup, tag_text):
        text_params = {}
        self._recursivr_inline_tag(tag_soup, tag_text, text_params)
        tag_name = tag_soup.name.lower() if tag_soup.name else ""
        if tag_name == 'a':
            href = tag_soup.get('href', "")
            if not href:
                logger.warning("Link href is empty")
            text_params["url"] = href
            text_obj = self.generate_link(**text_params)
        else:
            text_obj = self.generate_text(**text_params)
        return text_obj

    def get_block_type(self, single_tag):
        tag_name = single_tag.name
        style = single_tag.get('style') if tag_name else ""

        if tag_name == 'ol':
            return Block.NUMBERED_LIST.value
        if tag_name == 'ul':
            return Block.BULLETED_LIST.value

        if not style and tag_name == 'div':
            return Block.PARAGRAPH.value
        css_dict = {rule.split(':')[0].strip(): rule.split(
            ':')[1].strip() for rule in style.split(';') if rule}
        en_codeblock = css_dict.get('-en-codeblock', None)
        if en_codeblock == 'true':
            return Block.QUOTE.value


Html2JsonBase.register(YinXiang_Type, Html2JsonYinXiang)
