from html2notion.translate.html2json import Html2Json
import json
import os


def _check_convert_succ(case_name):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    json_file = os.path.join(script_dir, f"../demos/{case_name}.json")
    with open(json_file, "r") as f:
        result = json.load(f)

    html_file = os.path.join(script_dir, f"../demos/{case_name}.html")
    html2json = Html2Json(html_file)
    html2json.convert()
    convert = json.dumps(html2json.children)

    return convert == result


def test_html2json():
    assert _check_convert_succ("paragram_simple")

if __name__ == '__main__':
    test_html2json()