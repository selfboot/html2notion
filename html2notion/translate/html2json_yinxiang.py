from ..utils import logger
from ..translate.html2json_base import Html2JsonBase
from bs4 import BeautifulSoup


YinXiang_Type = "yinxiang"


class Html2JsonYinXiang(Html2JsonBase):
    input_type = YinXiang_Type

    def __init__(self, html_content):
        super().__init__(html_content)
        self.tag_map = {
            "div": "paragraph",
            "span": "text",
            "font": "text"
        }

    def process(self):
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
            if child.name is None:
                continue

            tagname = child.name.lower()
            if tagname in self.tag_map:
                tag_text = child.get_text()
                text_obj = {
                    "type": self.tag_map[tagname],
                    "text": {
                        "content": tag_text
                    }
                }
                rich_text.append(text_obj)

        return json_obj


Html2JsonBase.register(YinXiang_Type, Html2JsonYinXiang)
