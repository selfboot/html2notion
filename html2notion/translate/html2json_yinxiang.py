import cssutils
from bs4 import BeautifulSoup
from ..utils import logger
from ..translate.html2json_base import Html2JsonBase


YinXiang_Type = "yinxiang"


class Html2JsonYinXiang(Html2JsonBase):
    input_type = YinXiang_Type

    def __init__(self, html_content):
        super().__init__(html_content)
        self.tag_map = {
            # "div": "paragraph",
            "span": "text",
            "font": "text",
            "strike": "text",
        }

    def process(self):
        self.convert()
        return YinXiang_Type

    def convert(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        paragraphs = soup.find_all('div', recursive=True)

        for child in paragraphs:
            is_dup = False
            for parent in child.find_parents():
                if parent.name == 'div':
                    logger.debug("Filter child div")
                    is_dup = True
                    break
            if is_dup:
                continue
            parapraph = self.convert_paragraph(child)
            if parapraph:
                self.children.append(parapraph)

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
            tag_name = child.name.lower() if child.name else ""
            tag_text = child.text if child.text else ""
            if not tag_text:
                continue
            style = child.get('style') if child.name else ""
            tag_style = cssutils.parseStyle(style)
            text_obj = self.parse_tag(tag_name, tag_text, tag_style)
            if text_obj:
                rich_text.append(text_obj)

        return json_obj

    def parse_tag(self, tag_name, tag_text, styles):
        text_params = {}
        text_params["plain_text"] = tag_text
        if Html2JsonBase.is_bold(tag_name, styles):
            text_params["bold"] = True
        if Html2JsonBase.is_italic(tag_name, styles):
            text_params["italic"] = True
        if Html2JsonBase.is_strikethrough(tag_name, styles):
            text_params["strikethrough"] = True
        if Html2JsonBase.is_underline(tag_name, styles):
            text_params["underline"] = True

        color = Html2JsonBase.get_color(styles)
        if color != 'default':
            text_params["color"] = color
        text_obj = self.generate_text(**text_params)
        return text_obj


Html2JsonBase.register(YinXiang_Type, Html2JsonYinXiang)
