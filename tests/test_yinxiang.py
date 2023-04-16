import json
from pathlib import Path
from html2notion.translate.html2json_yinxiang import Html2JsonYinXiang
from bs4 import BeautifulSoup

# <a href='https://google.com'>Google</a>
link_rich_text = [{
    "href": "https://google.com",
    "plain_text": "Google",
    "text": {
        "link": {
            "url": "https://google.com"
        },
        "content": "Google"
    },
    "type": "text"
}]


def test_convert_paragraph():
    html_jsons = {
        "<a href='https://google.com'>Google</a>": link_rich_text
    }

    for html_content in html_jsons:
        yinxiang = Html2JsonYinXiang(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        json_obj = yinxiang.convert_paragraph(soup)
        assert json_obj["paragraph"]["rich_text"] == html_jsons[html_content]
