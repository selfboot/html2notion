from ..translate import Html2Json
import json
import os

def _check_convert_succ(case_name):
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)

    html_file = os.path.join(script_dir, f"../demos/{case_name}.html")
    json_file = os.path.join(script_dir, f"../demos/{case_name}.json")

    html2json = Html2Json(html_file)
    html2json.convert()
    convert = json.dumps(html2json.children)


def test_html2json():
    assert _check_convert_succ("paragram_simple")
