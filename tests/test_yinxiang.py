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

quote_content = '<div style="box-sizing: border-box; padding: 8px; font-family: Monaco, Menlo, Consolas, &quot;Courier New&quot;, monospace; font-size: 12px; color: rgb(51, 51, 51); border-radius: 4px; background-color: rgb(251, 250, 248); border: 1px solid rgba(0, 0, 0, 0.15);-en-codeblock:true;"><div>Quote 1</div><div>Quote 2</div><div>Quote 3</div><div><font color="#ff2600">Quote 4(red)</font></div></div>'
quote_block = [
    {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [
                {
                    "plain_text": "Quote 1\nQuote 2\nQuote 3\n",
                    "text": {
                        "content": "Quote 1\nQuote 2\nQuote 3\n"
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Quote 4(red)",
                    "text": {
                        "content": "Quote 4(red)"
                    },
                    "annotations": {
                        "color": "red"
                    },
                    "type": "text"
                }
            ]
        }
    }
]

quote_multi_paragram = """
<div style="box-sizing: border-box; padding: 8px; font-family: Monaco, Menlo, Consolas, &quot;Courier New&quot;, monospace; font-size: 12px; color: rgb(51, 51, 51); border-radius: 4px; background-color: rgb(251, 250, 248); border: 1px solid rgba(0, 0, 0, 0.15);-en-codeblock:true;"><div>Our models understand and process text by breaking it down into tokens. <font color="#ff9300">Tokens can be words or just chunks of characters.</font> For example, the word “hamburger” gets broken up into the tokens “ham”, “bur” and “ger”, while a short and common word like “pear” is a single token. Many tokens start with a whitespace, for example “ hello” and “ bye”.</div><div><br/></div><div>The number of tokens processed in a given API request depends on the length of both your inputs and outputs. As a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text. One limitation to keep in mind is that your text prompt and generated completion combined must be no more than the model's maximum context length (for most models this is 2048 tokens, or about 1500 words). Check out our <a href="https://platform.openai.com/tokenizer">tokenizer tool</a> to learn more about how text translates to tokens.</div></div>"""

quote_multi_paragram_block = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": []
        }
    },
    {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [
                {
                    "plain_text": "Our models understand and process text by breaking it down into tokens. ",
                    "text": {
                        "content": "Our models understand and process text by breaking it down into tokens. "
                    },
                    "type": "text"
                },
                {
                    "plain_text": "Tokens can be words or just chunks of characters.",
                    "text": {
                        "content": "Tokens can be words or just chunks of characters."
                    },
                    "annotations": {
                        "color": "orange"
                    },
                    "type": "text"
                },
                {
                    "plain_text": " For example, the word \u201chamburger\u201d gets broken up into the tokens \u201cham\u201d, \u201cbur\u201d and \u201cger\u201d, while a short and common word like \u201cpear\u201d is a single token. Many tokens start with a whitespace, for example \u201c hello\u201d and \u201c bye\u201d.\n\nThe number of tokens processed in a given API request depends on the length of both your inputs and outputs. As a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text. One limitation to keep in mind is that your text prompt and generated completion combined must be no more than the model's maximum context length (for most models this is 2048 tokens, or about 1500 words). Check out our ",
                    "text": {
                        "content": " For example, the word \u201chamburger\u201d gets broken up into the tokens \u201cham\u201d, \u201cbur\u201d and \u201cger\u201d, while a short and common word like \u201cpear\u201d is a single token. Many tokens start with a whitespace, for example \u201c hello\u201d and \u201c bye\u201d.\n\nThe number of tokens processed in a given API request depends on the length of both your inputs and outputs. As a rough rule of thumb, 1 token is approximately 4 characters or 0.75 words for English text. One limitation to keep in mind is that your text prompt and generated completion combined must be no more than the model's maximum context length (for most models this is 2048 tokens, or about 1500 words). Check out our "
                    },
                    "type": "text"
                },
                {
                    "href": "https://platform.openai.com/tokenizer",
                    "plain_text": "tokenizer tool",
                    "text": {
                        "link": {
                            "url": "https://platform.openai.com/tokenizer"
                        },
                        "content": "tokenizer tool"
                    },
                    "type": "text"
                },
                {
                    "plain_text": " to learn more about how text translates to tokens.",
                    "text": {
                        "content": " to learn more about how text translates to tokens."
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


def test_convert():
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf, logger
        test_prepare_conf()
        logger.info("prepare_conf_fixture")

    html_jsons = {
        link_content: link_block,
        order_list_content: ordered_list_block,
        nested_bold_content: nested_bold_block,
        quote_content: quote_block,
        quote_multi_paragram: quote_multi_paragram_block,
        paragram_rich_content: paragram_rich_block
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
