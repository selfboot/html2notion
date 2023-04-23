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

paragram_rich_content = '<div>Normal text<span style="color: rgb(255, 38, 0);">Red text</span>, <span style="color: rgb(0, 249, 0);">Green text</span>, <span style="color: rgb(170, 121, 66);">Gray text</span><span style="color: rgb(148, 33, 146);">Purple text</span>, <span style="color: rgb(255, 147, 0);">Orange text</span>, <span style="color: rgb(255, 251, 0);">Yellow text</span><a href="http://www.baidu.com/">Link</a>, <span style="text-decoration: underline;">Underline text</span>,<span style="font-weight: bold;">Bold text</span>,<span style="text-decoration: line-through;">Strikethrough text</span>,<span style="font-style: italic;">Italic text</span></div>'
paragram_rich_block = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "plain_text": "Normal text",
                    "text": {
                        "content": "Normal text"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Red text",
                    "text": {
                        "content": "Red text"
                    },
                    "annotations": {
                        "color": "red"
                    },
                    "type": "text"
                },
                {
                    "plain_text": ", ",
                    "text": {
                        "content": ", "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Green text",
                    "text": {
                        "content": "Green text"
                    },
                    "annotations": {
                        "color": "green"
                    },
                    "type": "text"
                },
                {
                    "plain_text": ", ",
                    "text": {
                        "content": ", "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Gray text",
                    "text": {
                        "content": "Gray text"
                    },
                    "annotations": {
                        "color": "gray"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Purple text",
                    "text": {
                        "content": "Purple text"
                    },
                    "annotations": {
                        "color": "purple"
                    },
                    "type": "text"
                },
                {
                    "plain_text": ", ",
                    "text": {
                        "content": ", "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Orange text",
                    "text": {
                        "content": "Orange text"
                    },
                    "annotations": {
                        "color": "orange"
                    },
                    "type": "text"
                },
                {
                    "plain_text": ", ",
                    "text": {
                        "content": ", "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Yellow text",
                    "text": {
                        "content": "Yellow text"
                    },
                    "annotations": {
                        "color": "yellow"
                    },
                    "type": "text"
                },
                {
                    "href": "http://www.baidu.com/",
                    "plain_text": "Link",
                    "text": {
                        "link": {
                            "url": "http://www.baidu.com/"
                        },
                        "content": "Link"
                    },
                    "type": "text"
                },
                {
                    "plain_text": ", ",
                    "text": {
                        "content": ", "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Underline text",
                    "text": {
                        "content": "Underline text"
                    },
                    "annotations": {
                        "underline": True
                    },
                    "type": "text"
                },
                {
                    "plain_text": ",",
                    "text": {
                        "content": ","
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Bold text",
                    "text": {
                        "content": "Bold text"
                    },
                    "annotations": {
                        "bold": True
                    },
                    "type": "text"
                },
                {
                    "plain_text": ",",
                    "text": {
                        "content": ","
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Strikethrough text",
                    "text": {
                        "content": "Strikethrough text"
                    },
                    "annotations": {
                        "strikethrough": True
                    },
                    "type": "text"
                },
                {
                    "plain_text": ",",
                    "text": {
                        "content": ","
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Italic text",
                    "text": {
                        "content": "Italic text"
                    },
                    "annotations": {
                        "italic": True
                    },
                    "type": "text"
                }
            ]
        }
    }
]

heading_content = '<h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6>'
heading_block = [
    {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [
                {
                    "plain_text": "Heading 1",
                    "text": {
                        "content": "Heading 1"
                    },
                    "type": "text"
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [
                {
                    "plain_text": "Heading 2",
                    "text": {
                        "content": "Heading 2"
                    },
                    "type": "text"
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [
                {
                    "plain_text": "Heading 3",
                    "text": {
                        "content": "Heading 3"
                    },
                    "type": "text"
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [
                {
                    "plain_text": "Heading 4",
                    "text": {
                        "content": "Heading 4"
                    },
                    "type": "text"
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [
                {
                    "plain_text": "Heading 5",
                    "text": {
                        "content": "Heading 5"
                    },
                    "type": "text"
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [
                {
                    "plain_text": "Heading 6",
                    "text": {
                        "content": "Heading 6"
                    },
                    "type": "text"
                }
            ]
        }
    }
]


code_content = '<div style="-en-codeblock:true;"><div>Code Line 1</div><div>Code Line 2</div><div>Code Line 3</div><div><font color="#ff2600">Code Line 4(red)</font></div></div>'
code_block = [
    {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [
                {
                    "plain_text": "Code Line 1\nCode Line 2\nCode Line 3\n",
                    "text": {
                        "content": "Code Line 1\nCode Line 2\nCode Line 3\n"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Code Line 4(red)",
                    "text": {
                        "content": "Code Line 4(red)"
                    },
                    "type": "text",
                    "annotations": {
                        "color": "red"
                    }
                }
            ],
            "language": "plain text"
        }
    }
]

language_code_content = '<div style="--en-codeblock:true;--en-codeblockLanguage:python;">import os\nprint("hello")</div>'
language_code_block = [
    {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [
                {
                    "plain_text": "import os\nprint(\"hello\")",
                    "text": {
                        "content": "import os\nprint(\"hello\")"
                    },
                    "type": "text"
                }
            ],
            "language": "python"
        }
    }
]
    
def test_convert():
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf, logger
        test_prepare_conf()
        logger.info("prepare_conf_fixture")

    html_jsons = {
        link_content: link_block,
        order_list_content: ordered_list_block,
        nested_bold_content: nested_bold_block,
        paragram_rich_content: paragram_rich_block,
        heading_content: heading_block,
        code_content: code_block,
        language_code_content: language_code_block
    }

    for html_content in html_jsons:
        body_content = '<body>' + html_content + '</body>'
        yinxiang = Html2JsonYinXiang(body_content)
        yinxiang.process()
        json_obj = yinxiang.children
        print(json.dumps(json_obj, indent=4))
        # assert json_obj == html_jsons[html_content]


if __name__ == '__main__':
    test_convert()
