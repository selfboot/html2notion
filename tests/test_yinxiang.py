import json
import os
from html2notion.translate.html2json_yinxiang import Html2JsonYinXiang

link_content = "<div><a href='https://google.com'>Google</a></div>"
link_block = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "href": "https://google.com",
                    "plain_text": "Google",
                    "text": {
                        "link": {
                            "url": "https://google.com"
                        },
                        "content": "Google"
                    },
                    "type": "text"
                }
            ]
        }
    }
]

order_list_content = '<ol><li><div>first</div></li><li><div>second</div></li><li><div>third</div></li></ol>'
ordered_list_block = [
    {
        "object": "block",
        "numbered_list_item": {
            "rich_text": [
                {
                    "plain_text": "first",
                    "text": {
                        "content": "first"
                    },
                    "type": "text"
                }
            ]
        },
        "type": "numbered_list_item"
    },
    {
        "object": "block",
        "numbered_list_item": {
            "rich_text": [
                {
                    "plain_text": "second",
                    "text": {
                        "content": "second"
                    },
                    "type": "text"
                }
            ]
        },
        "type": "numbered_list_item"
    },
    {
        "object": "block",
        "numbered_list_item": {
            "rich_text": [
                {
                    "plain_text": "third",
                    "text": {
                        "content": "third"
                    },
                    "type": "text"
                }
            ]
        },
        "type": "numbered_list_item"
    }
]

nested_bold_content = '<div><b><u>underline bold</u></b></div>'
nested_bold_block = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "plain_text": "underline bold",
                    "text": {
                        "content": "underline bold"
                    },
                    "annotations": {
                        "bold": True,
                        "underline": True
                    },
                    "type": "text"
                }
            ]
        }
    }
]


def test_convert():
    html_jsons = {
        link_content: link_block,
        order_list_content: ordered_list_block,
        nested_bold_content: nested_bold_block
    }

    for html_content in html_jsons:
        body_content = '<body>' + html_content + '</body>'
        yinxiang = Html2JsonYinXiang(body_content)
        yinxiang.convert()
        json_obj = yinxiang.children
        # print(json.dumps(json_obj, indent=4))
        assert json_obj == html_jsons[html_content]


if __name__ == '__main__':
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import config, test_prepare_conf
        test_prepare_conf()
    test_convert()
