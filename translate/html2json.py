from ..utils import logger
from bs4 import BeautifulSoup
import os
import json


class Html2Json:
    def __init__(self, html_file):
        self.tag_map = {
            "div": "paragraph",
            "span": "text",
            "font": "text"
        }
        self.attr_map = {
            "color": "color",
            "size": "font_size",
        }

        self.children = []
        self.html_file = html_file
        self.html_content = ""

        if not os.path.exists(html_file):
            logger.error("Load file failed", html_file)
        else:
            with open(self.html_file, "r") as file:
                self.html_content = file.read()

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
                tag_value = self.tag_map[tagname]
                # parse annotation

                tag_text = child.get_text()
                text_obj = {
                    "type": self.tag_map[tagname],
                    "text": {
                        "content": tag_text
                    }
                }
                rich_text.append(text_obj)

        return json_obj

    def get_res(self):
        return self.children


if __name__ == "__main__":
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    html_test = os.path.join(script_dir, "../demos/paragram_simple.html")
    html2json = Html2Json(html_test)
    html2json.convert()
    print(json.dumps(html2json.children, indent=4))
