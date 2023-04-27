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
                    "type": "text",
                    "annotations": {
                        "color": "red"
                    }
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
                    "type": "text",
                    "annotations": {
                        "color": "green"
                    }
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
                    "type": "text",
                    "annotations": {
                        "color": "gray"
                    }
                },
                {
                    "plain_text": "Purple text",
                    "text": {
                        "content": "Purple text"
                    },
                    "type": "text",
                    "annotations": {
                        "color": "purple"
                    }
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
                    "type": "text",
                    "annotations": {
                        "color": "orange"
                    }
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
                    "type": "text",
                    "annotations": {
                        "color": "yellow"
                    }
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
                    "type": "text",
                    "annotations": {
                        "underline": True
                    }
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
                    "type": "text",
                    "annotations": {
                        "bold": True
                    }
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
                    "type": "text",
                    "annotations": {
                        "strikethrough": True
                    }
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
                    "type": "text",
                    "annotations": {
                        "italic": True
                    }
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


code_content = '<div style="-en-codeblock:True;"><div>Code Line 1</div><div>Code Line 2</div><div>Code Line 3</div><div><font color="#ff2600">Code Line 4(red)</font></div></div>'
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

code_paragraph_content = '<div style="-en-codeblock:True;"><div>Quote 1</div><div>2</div><div>3</div><div><span style="color: rgb(255, 38, 0);">Read 4</span></div><div><span style="color: rgb(255, 38, 0);">5</span></div><div>6. <a href="https://openai.com/">OpenAI</a>’s mission is to create artificial intelligence systems that benefit everyone. To that end, we invest heavily in research and engineering to ensure our AI systems are safe and secure. However, as with any <font color="#942192"><b>complex technology</b></font>, we understand that vulnerabilities and flaws can emerge.</div></div>'
code_paragraph_block = [
    {
        "object": "block",
        "type": "code",
        "code": {
            "rich_text": [
                {
                    "plain_text": "Quote 1\n2\n3\n",
                    "text": {
                        "content": "Quote 1\n2\n3\n"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Read 4",
                    "text": {
                        "content": "Read 4"
                    },
                    "type": "text",
                    "annotations": {
                        "color": "red"
                    }
                },
                {
                    "plain_text": "\n",
                    "text": {
                        "content": "\n"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "5",
                    "text": {
                        "content": "5"
                    },
                    "type": "text",
                    "annotations": {
                        "color": "red"
                    }
                },
                {
                    "plain_text": "\n6. ",
                    "text": {
                        "content": "\n6. "
                    },
                    "type": "text"
                },
                {
                    "href": "https://openai.com/",
                    "plain_text": "OpenAI",
                    "text": {
                        "link": {
                            "url": "https://openai.com/"
                        },
                        "content": "OpenAI"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "\u2019s mission is to create artificial intelligence systems that benefit everyone. To that end, we invest heavily in research and engineering to ensure our AI systems are safe and secure. However, as with any ",
                    "text": {
                        "content": "\u2019s mission is to create artificial intelligence systems that benefit everyone. To that end, we invest heavily in research and engineering to ensure our AI systems are safe and secure. However, as with any "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "complex technology",
                    "text": {
                        "content": "complex technology"
                    },
                    "type": "text",
                    "annotations": {
                        "color": "purple",
                        "bold": True
                    }
                },
                {
                    "plain_text": ", we understand that vulnerabilities and flaws can emerge.",
                    "text": {
                        "content": ", we understand that vulnerabilities and flaws can emerge."
                    },
                    "type": "text"
                }
            ],
            "language": "plain text"
        }
    }
]

language_code_content = '<div style="--en-codeblock:True;--en-codeblockLanguage:python;">import os\nprint("hello")</div>'
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

table_content = '<div><div><br /></div><table><tbody><tr><td><div>Row 1:<span style="color: rgb(0, 166, 125);">You are a helpful assistant.</span> Rember it.</div></td><td><div>Row 1:<a href="https://platform.openai.com/docs/guides/chat/introduction" >https://platform.openai.com/docs/guides/chat/introduction</a></div></td><td><div>Row 1:<b><u>Import Content</u></b> Read more.</div></td></tr><tr><td><div>Row 2:</div></td><td><div>Row 2:</div></td><td><div>Row 2:</div></td></tr></tbody></table><div><br /></div></div>'
super_note_table_content = '<table><tbody><tr><td><div>Row 1:<span style="color: rgb(0, 166, 125);">You are a helpful assistant.</span> Rember it.</div></td><td><div>Row 1:<a href="https://platform.openai.com/docs/guides/chat/introduction" >https://platform.openai.com/docs/guides/chat/introduction</a></div></td><td><div>Row 1:<b><u>Import Content</u></b> Read more.</div></td></tr><tr><td><div>Row 2:</div></td><td><div>Row 2:</div></td><td><div>Row 2:</div></td></tr></tbody></table>'
table_block = [
    {
        "table": {
            "has_row_header": False,
            "has_column_header": False,
            "table_width": 3,
            "children": [
                {
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            [
                                {
                                    "plain_text": "Row 1:",
                                    "text": {
                                        "content": "Row 1:"
                                    },
                                    "type": "text"
                                },
                                {
                                    "plain_text": "You are a helpful assistant.",
                                    "text": {
                                        "content": "You are a helpful assistant."
                                    },
                                    "type": "text",
                                    "annotations": {
                                        "color": "green"
                                    }
                                },
                                {
                                    "plain_text": " Rember it.",
                                    "text": {
                                        "content": " Rember it."
                                    },
                                    "type": "text"
                                }
                            ],
                            [
                                {
                                    "plain_text": "Row 1:",
                                    "text": {
                                        "content": "Row 1:"
                                    },
                                    "type": "text"
                                },
                                {
                                    "href": "https://platform.openai.com/docs/guides/chat/introduction",
                                    "plain_text": "https://platform.openai.com/docs/guides/chat/introduction",
                                    "text": {
                                        "link": {
                                            "url": "https://platform.openai.com/docs/guides/chat/introduction"
                                        },
                                        "content": "https://platform.openai.com/docs/guides/chat/introduction"
                                    },
                                    "type": "text"
                                }
                            ],
                            [
                                {
                                    "plain_text": "Row 1:",
                                    "text": {
                                        "content": "Row 1:"
                                    },
                                    "type": "text"
                                },
                                {
                                    "plain_text": "Import Content",
                                    "text": {
                                        "content": "Import Content"
                                    },
                                    "type": "text",
                                    "annotations": {
                                        "bold": True,
                                        "underline": True
                                    }
                                },
                                {
                                    "plain_text": " Read more.",
                                    "text": {
                                        "content": " Read more."
                                    },
                                    "type": "text"
                                }
                            ]
                        ]
                    }
                },
                {
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            [
                                {
                                    "plain_text": "Row 2:",
                                    "text": {
                                        "content": "Row 2:"
                                    },
                                    "type": "text"
                                }
                            ],
                            [
                                {
                                    "plain_text": "Row 2:",
                                    "text": {
                                        "content": "Row 2:"
                                    },
                                    "type": "text"
                                }
                            ],
                            [
                                {
                                    "plain_text": "Row 2:",
                                    "text": {
                                        "content": "Row 2:"
                                    },
                                    "type": "text"
                                }
                            ]
                        ]
                    }
                }
            ]
        }
    }
]

to_do_content = '''<ul style=""><li style=""><div><input type="checkbox"/>Choose classes that map to a single <a href="https://platform.openai.com/tokenizer" rev="en_rl_none">token</a>. At inference time, specify <span style="font-weight: 500;">max_tokens=1</span> since you only need the first token for classification.</div></li><li style=""><div><input type="checkbox"/>Use a separator at the end of the prompt, e.g. <code style="-en-code: true"><span style="font-weight: 500;">\n\n###\n\n</span></code>.Remember to also append this separator when you eventually make requests to your model.</div></li><li style=""><div><input checked="true" type="checkbox"/>Ensure that the prompt + completion doesn't exceed 2048 tokens, including the separator</div></li></ul>'''
to_do_normal_content = '''<div><input type="checkbox"/>Choose classes that map to a single <a href="https://platform.openai.com/tokenizer" rev="en_rl_none">token</a>. At inference time, specify <span style="font-weight: 500;">max_tokens=1</span> since you only need the first token for classification.</div><div><input type="checkbox"/>Use a separator at the end of the prompt, e.g. <code style="-en-code: true"><span style="font-weight: 500;">\n\n###\n\n</span></code>.Remember to also append this separator when you eventually make requests to your model.</div><div><input checked="true" type="checkbox"/>Ensure that the prompt + completion doesn't exceed 2048 tokens, including the separator</div>'''
to_do_block = [
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {
                    "plain_text": "Choose classes that map to a single\u00a0",
                    "text": {
                        "content": "Choose classes that map to a single\u00a0"
                    },
                    "type": "text"
                },
                {
                    "href": "https://platform.openai.com/tokenizer",
                    "plain_text": "token",
                    "text": {
                        "link": {
                            "url": "https://platform.openai.com/tokenizer"
                        },
                        "content": "token"
                    },
                    "type": "text"
                },
                {
                    "plain_text": ". At inference time, specify\u00a0",
                    "text": {
                        "content": ". At inference time, specify\u00a0"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "max_tokens=1",
                    "text": {
                        "content": "max_tokens=1"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "\u00a0since you only need the first token for classification.",
                    "text": {
                        "content": "\u00a0since you only need the first token for classification."
                    },
                    "type": "text"
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {
                    "plain_text": "Use a separator at the end of the prompt, e.g.\u00a0",
                    "text": {
                        "content": "Use a separator at the end of the prompt, e.g.\u00a0"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "\n\n###\n\n",
                    "text": {
                        "content": "\n\n###\n\n"
                    },
                    "type": "text",
                    "annotations": {
                        "code": True
                    }
                },
                {
                    "plain_text": ".Remember to also append this separator when you eventually make requests to your model.",
                    "text": {
                        "content": ".Remember to also append this separator when you eventually make requests to your model."
                    },
                    "type": "text"
                }
            ],
            "checked": False
        }
    },
    {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [
                {
                    "plain_text": "Ensure that the prompt + completion doesn't exceed 2048 tokens, including the separator",
                    "text": {
                        "content": "Ensure that the prompt + completion doesn't exceed 2048 tokens, including the separator"
                    },
                    "type": "text"
                }
            ],
            "checked": True
        }
    }
]

divider_content = '<hr/>'
divider_block = [
    {
        "object": "block",
        "type": "divider",
        "divider": {}
    }
]

quote_content = """<div style="--en-blockquote:true;box-sizing: border-box; padding-left: 19px; padding-top: 6px; padding-bottom: 6px; border-left: 3px solid #b4c0cc; background-position: initial initial; background-repeat: initial initial; margin-top: 6px"><div>We recommend completing our quickstart tutorial to get acquainted with key concepts through a <span style="color: #9B00FF;">hands-on, interactive example</span>.</div><div><br/></div><div>First, you’ll need a prompt that makes it clear what you want. Let’s start with an instruction. <b>Submit this prompt</b> to generate your first completion.</div></div>"""
quote_block = [
    {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [
                {
                    "plain_text": "We recommend completing our quickstart tutorial to get acquainted with key concepts through a ",
                    "text": {
                        "content": "We recommend completing our quickstart tutorial to get acquainted with key concepts through a "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "hands-on, interactive example",
                    "text": {
                        "content": "hands-on, interactive example"
                    },
                    "type": "text",
                    "annotations": {
                        "color": "purple"
                    }
                },
                {
                    "plain_text": ".\n\nFirst, you\u2019ll need a prompt that makes it clear what you want. Let\u2019s start with an instruction.\u00a0",
                    "text": {
                        "content": ".\n\nFirst, you\u2019ll need a prompt that makes it clear what you want. Let\u2019s start with an instruction.\u00a0"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Submit this prompt",
                    "text": {
                        "content": "Submit this prompt"
                    },
                    "type": "text",
                    "annotations": {
                        "bold": True
                    }
                },
                {
                    "plain_text": "\u00a0to generate your first completion.",
                    "text": {
                        "content": "\u00a0to generate your first completion."
                    },
                    "type": "text"
                }
            ]
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
        code_paragraph_content: code_paragraph_block,
        language_code_content: language_code_block,
        table_content: table_block,
        super_note_table_content: table_block,
        to_do_content: to_do_block,
        to_do_normal_content: to_do_block,
        divider_content: divider_block,
        quote_content: quote_block,
    }

    for html_content in html_jsons:
        body_content = '<body>' + html_content + '</body>'
        yinxiang = Html2JsonYinXiang(body_content)
        yinxiang.process()
        json_obj = yinxiang.children
        # print(json.dumps(json_obj, indent=4))
        assert json_obj == html_jsons[html_content]


if __name__ == '__main__':
    test_convert()
