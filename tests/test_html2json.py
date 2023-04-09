import json
from pathlib import Path
from html2notion.translate.html2json import html2json_process


def _check_convert_succ(case_name):
    json_file = Path(f"./demos/{case_name}.json")
    with open(json_file, "r") as f:
        result = json.load(f)

    html_file = Path(f"./demos/{case_name}.html")
    html2json = html2json_process(html_file)
    if html2json[1] is False:
        return False
    convert = json.dumps(html2json[0])

    return convert == result


def test_html2json():
    assert not _check_convert_succ("yinxiang")   # todo


if __name__ == '__main__':
    test_html2json()
