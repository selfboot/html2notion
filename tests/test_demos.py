# import glob
import json
import os
from pathlib import Path
from html2notion.translate.html2json import html2json_process
from html2notion.translate.import_stats import ImportStats
from html2notion.translate.html2json_markdown import YinXiangMarkdown_Type
from html2notion.utils import logger, config


def test_demo_files():
    if 'GITHUB_ACTIONS' in os.environ:
        database_id = os.environ['notion_db_id_1']
    else:
        database_id = config['notion']['database_id']

    # md_files = glob.glob("tests/demo_files/*.html")
    md_file = Path("./demos/yinxiang_markdown.html")
    import_stats = ImportStats()
    notion_data, html_type = html2json_process(md_file, import_stats)

    assert html_type == YinXiangMarkdown_Type
    with open("./demos/yinxiang_markdown.json", "r") as f:
        content = f.read()

    content = content.replace("###database_id###", database_id)  # Replace the placeholder
    expect = json.loads(content)

    # The timezone causes the calculated time to be different, and the check here can be ignored
    try:
        del expect['properties']['Created']['date']['start']
        del notion_data['properties']['Created']['date']['start']
    except KeyError as e:
        pass
    assert notion_data == expect
