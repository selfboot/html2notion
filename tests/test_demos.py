# import glob
import json
import os
from pathlib import Path
from html2notion.translate.html2json import html2json_process
from html2notion.translate.import_stats import ImportStats
from html2notion.translate.html2json_markdown import YinXiangMarkdown_Type
from html2notion.translate.html2json_clipper import YinXiangClipper_Type
from html2notion.utils import logger, config


def test_demo_files():
    if 'GITHUB_ACTIONS' in os.environ:
        database_id = os.environ['notion_db_id_1']
    else:
        database_id = config['notion']['database_id']

    testcases = [
        ["./demos/yinxiang_markdown.html", YinXiangMarkdown_Type, "./demos/yinxiang_markdown.json"],
        ["./demos/yinxiang_clipper.html", YinXiangClipper_Type, "./demos/yinxiang_clipper.json"],
        ["./demos/yinxiang_clipper_wx.html", YinXiangClipper_Type, "./demos/yinxiang_clipper_wx.json"],
    ]

    for md_file, expect_type, expect_file in testcases:
        import_stats = ImportStats()
        notion_data, html_type = html2json_process(Path(md_file), import_stats)

        assert html_type == expect_type
        with open(expect_file, "r") as f:
            content = f.read()

        # Replace the placeholder
        content = content.replace("###database_id###", database_id)
        expect = json.loads(content)

        # The timezone causes the calculated time to be different, and the check here can be ignored
        try:
            del expect['properties']['Created']['date']['start']
            del notion_data['properties']['Created']['date']['start']
        except KeyError as e:
            pass
        
        # import dictdiffer
        # diff = dictdiffer.diff(notion_data, expect)
        # for d in diff:
        #     logger.debug(f'Diff: {d}')
        # aa = json.dumps(notion_data, ensure_ascii=False)
        # logger.debug(f'notion_data: {aa}')
        assert notion_data ==expect 

