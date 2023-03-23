from html2notion.translate.html2json import Html2Json
import json
from pathlib import Path


def _check_convert_succ(case_name):
    json_file = Path(f"./demos/{case_name}.json")
    with open(json_file, "r") as f:
        result = json.load(f)

    html_file = Path(f"./demos/{case_name}.html")
    html2json = Html2Json(html_file)
    html2json.convert()
    convert = json.dumps(html2json.children)

    return convert == result


def test_html2json():
    assert not _check_convert_succ("paragram_simple")   # todo


if __name__ == '__main__':
    test_html2json()
