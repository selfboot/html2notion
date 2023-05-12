import json
import chardet
import time
from functools import singledispatch
from pathlib import Path
from bs4 import BeautifulSoup, Tag
from ..utils import logger, test_prepare_conf
from ..translate.html2json_base import Html2JsonBase
from ..translate.html2json_default import Default_Type
from ..translate.html2json_yinxiang import YinXiang_Type
from ..translate.html2json_clipper import YinXiangClipper_Type
from ..translate.html2json_markdown import YinXiangMarkdown_Type


"""
<meta name="source" content="yinxiang.superNote"/>
<meta name="source" content="desktop.mac"/>
<meta name="source" content="mobile.android"/>
"""
def _is_yinxiang_export_html(html_soup):
    meta_source = html_soup.select_one('html > head > meta[name="source"]')
    meta_source_content = meta_source.get('content', "") if isinstance(meta_source, Tag) else ""
    yinxiang_source_content = ["yinxiang", "desktop", "mobile"]
    for prefix in yinxiang_source_content:
        if isinstance(meta_source_content, str) and meta_source_content.startswith(prefix):
            return True
    return False


"""
<meta name="source-application" content="webclipper.evernote" />
<meta name="source-application" content="微信" />
"""
def _is_yinxiang_clipper_html(html_soup):
    meta_source_application = html_soup.select_one('html > head > meta[name="source-application"]')
    source_application = meta_source_application.get('content', "") if isinstance(meta_source_application, Tag) else ""
    if isinstance(source_application, str) and source_application.endswith("evernote"):
        return True
    if isinstance(source_application, str) and source_application in ["微信",]:
        return True
    return False


"""
<meta name="content-class" content="yinxiang.markdown" />
"""
def _is_yinxiang_markdown_html(html_soup):
    meta_content_class = html_soup.select_one('html > head > meta[name="content-class"]')
    content_class = meta_content_class.get('content', "") if isinstance(meta_content_class, Tag) else ""
    if isinstance(content_class, str) and content_class.endswith("markdown"):
        return True
    return False


def _infer_input_type(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    exporter_version_meta = soup.select_one('html > head > meta[name="exporter-version"]')
    exporter_version_content = exporter_version_meta.get(
        'content', "") if isinstance(
        exporter_version_meta, Tag) else ""

    # yinxiang export
    if isinstance(exporter_version_content, str) and exporter_version_content.startswith("Evernote"):
        if _is_yinxiang_markdown_html(soup):
            return YinXiangMarkdown_Type
        if _is_yinxiang_clipper_html(soup):
            return YinXiangClipper_Type
        elif _is_yinxiang_export_html(soup):
            return YinXiang_Type

    return Default_Type


def _get_converter(html_content, import_stat):
    html_type = _infer_input_type(html_content)
    logger.info(f"Input type: {html_type}")
    converter = Html2JsonBase.create(html_type, html_content, import_stat)
    return converter


@singledispatch
def html2json_process(html_content, import_stat):
    raise TypeError(f"Unsupported {type(html_content)}, {import_stat}")


@html2json_process.register
def _(html_content: str, import_stat):
    converter = _get_converter(html_content, import_stat)
    result = converter.process()
    return converter.get_notion_data(), result


@html2json_process.register
def _(html_file: Path, import_stat):
    if not html_file.is_file():
        print(f"Load file: {html_file.resolve()} failed")
        raise FileNotFoundError

    html_content = ""
    with html_file.open('rb') as f:
        data = f.read()
        result = chardet.detect(data)
        encoding = result['encoding'] if result['encoding'] else 'utf-8'
        html_content = data.decode(encoding)

        if html_content == "main_hold":                  # just for local debug
            time.sleep(1)
            return "main_hold"

    converter = _get_converter(html_content, import_stat)
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
