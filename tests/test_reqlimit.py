import json
from html2notion.translate.html2json_yinxiang import Html2JsonYinXiang
from html2notion.translate.import_stats import ImportStats


block_max_conent = "Some words" * 200
one_text_obj = {
    "plain_text": block_max_conent,
    "text": {
        "content": block_max_conent
    },
    "type": "text"
}
remain_text_obj = {
    "plain_text": " more words",
    "text": {
        "content": " more words"
    },
    "type": "text"
}


def test_reqlimit():
    paragram_rich_block = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    one_text_obj, one_text_obj, remain_text_obj
                ]
            }
        }
    ]

    paragram_rich_content = f'<body><div>{block_max_conent * 2} more words</div></body>'
    import_stats = ImportStats()
    yinxiang = Html2JsonYinXiang(paragram_rich_content, import_stats)
    yinxiang.process()
    json_obj = yinxiang.children
    # print(json.dumps(json_obj, indent=4))
    assert json_obj == paragram_rich_block


def test_code_reqlimit():
    code_rich_content = f'<body><div style="-en-codeblock: true">{block_max_conent * 2} more words</div></body>'
    import_stats = ImportStats()
    yinxiang = Html2JsonYinXiang(code_rich_content, import_stats)
    yinxiang.process()
    json_obj = yinxiang.children
    # print(json.dumps(json_obj, indent=4))

    split_block_result = [
        {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [
                    one_text_obj, one_text_obj, remain_text_obj
                ],
                "language": "plain text"
            }
        }
    ]
    assert json_obj == split_block_result


if __name__ == '__main__':
    # test_reqlimit()
    test_code_reqlimit()
