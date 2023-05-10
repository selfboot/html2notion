import json
import os
from html2notion.translate.html2json_yinxiang import Html2JsonYinXiang
from html2notion.translate.import_stats import ImportStats


paragram_rich_content = f'<div>{"Some words" * 400} more words</div>'
block_max_conent = "Some words" * 200
paragram_rich_block = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "plain_text": block_max_conent,
                    "text": {
                        "content": block_max_conent
                    },
                    "type": "text"
                },
                {
                    "plain_text": block_max_conent,
                    "text": {
                        "content": block_max_conent
                    },
                    "type": "text"
                },
                {
                    "plain_text": " more words",
                    "text": {
                        "content": " more words"
                    },
                    "type": "text"
                }
            ]
        }
    }
]


def test_reqlimit():
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf, logger
        test_prepare_conf()
        logger.info("prepare_conf_fixture")

    html_jsons = {
        paragram_rich_content: paragram_rich_block,
    }

    for html_content in html_jsons:
        body_content = '<body>' + html_content + '</body>'
        import_stats = ImportStats()
        yinxiang = Html2JsonYinXiang(body_content, import_stats)
        yinxiang.process()
        json_obj = yinxiang.children
        # print(json.dumps(json_obj, indent=4))
        assert json_obj == html_jsons[html_content]


if __name__ == '__main__':
    test_reqlimit()
