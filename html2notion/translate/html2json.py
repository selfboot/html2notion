import sys
import json
from functools import singledispatch
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from ..utils import logger, test_prepare_conf
from ..translate.html2json_base import Html2JsonBase
from ..translate.html2json_default import Default_Type
from ..translate.html2json_yinxiang import YinXiang_Type
from ..translate.html2json_clipper import YinXiangClipper_Type


"""
<meta name="source" content="yinxiang.superNote"/>
<meta name="source" content="desktop.mac"/>
"""
def _is_yinxiang_export_html(html_soup):
    exporter_version_meta = html_soup.select_one('html > head > meta[name="exporter-version"]')
    meta_source = html_soup.select_one('html > head > meta[name="source"]')
    exporter_version_content = exporter_version_meta.get( 'content', "") if isinstance(exporter_version_meta, Tag) else ""

    meta_source_content = meta_source.get('content', "") if isinstance(meta_source, Tag) else ""
    if isinstance(exporter_version_content, str) and not exporter_version_content.startswith("Evernote"):
        return False

    yinxiang_source_content = ["yinxiang", "desktop", "web"]
    for prefix in yinxiang_source_content:
        if isinstance(meta_source_content, str) and meta_source_content.startswith(prefix):
            return True
    return False


"""
<meta name="source-application" content="webclipper.evernote" />
"""
def _is_yinxiang_clipper_html(html_soup):
    exporter_version_meta = html_soup.select_one('html > head > meta[name="exporter-version"]')
    exporter_version_content = exporter_version_meta.get(
        'content', "") if isinstance(
        exporter_version_meta, Tag) else ""

    if isinstance(exporter_version_content, str) and not exporter_version_content.startswith("Evernote"):
        return False
    clipper_source_meta = html_soup.select_one('html > head > meta[name="source-application"]')
    clipper_source_content = clipper_source_meta.get('content', "") if isinstance(clipper_source_meta, Tag) else ""
    if isinstance(clipper_source_content, str) and clipper_source_content.endswith("evernote"):
        return True
    return False


def _infer_input_type(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    if _is_yinxiang_export_html(soup):
        return YinXiang_Type
    elif _is_yinxiang_clipper_html(soup):
        return YinXiangClipper_Type
    return Default_Type


def _get_converter(html_content):
    html_type = _infer_input_type(html_content)
    logger.info(f"Input type: {html_type}")
    converter = Html2JsonBase.create(html_type, html_content)
    return converter


@singledispatch
def html2json_process(html_content):
    raise TypeError("Unsupported param type")


@html2json_process.register
def _(html_content: str):
    converter = _get_converter(html_content)
    result = converter.process()
    return converter.get_notion_data(), result


@html2json_process.register
def _(html_file: Path):
    if not html_file.is_file():
        print(f"Load file: {html_file.resolve()} failed")
        sys.exit(1)

    with open(html_file, "r") as file:
        html_content = file.read()

    converter = _get_converter(html_content)
    result = converter.process()
    return converter.get_notion_data(), result


if __name__ == "__main__":
    test_prepare_conf()
    html_file = Path("./demos/Test Case D.html")
    result, html_type = html2json_process(html_file)
    print(html_type)
    print(json.dumps(result, indent=4, ensure_ascii=False))
    result2, html_type2 = html2json_process(
        "<html><body><div>test</div></body></html>")
    print(html_type2)
    print(json.dumps(result2, indent=4, ensure_ascii=False))
