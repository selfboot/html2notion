import os
from functools import singledispatch
from pathlib import Path
from bs4 import BeautifulSoup
from ..utils import logger, test_prepare_conf
from ..translate.html2json_base import Html2JsonBase
from ..translate.html2json_default import Default_Type
from ..translate.html2json_yinxiang import YinXiang_Type


def _infer_input_type(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    exporter_version_meta = soup.find(
        'meta', attrs={'name': 'exporter-version'})
    exporter_version_content = exporter_version_meta.get(
        'content') if exporter_version_meta else None
    if exporter_version_content and exporter_version_content.startswith("Evernote"):
        return YinXiang_Type

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
    return converter.get_res(), result


@html2json_process.register
def _(html_file:  Path):
    if not html_file.is_file():
        print(f"Load file: {html_file.resolve()} failed")
        os.exit(1)

    with open(html_file, "r") as file:
        html_content = file.read()

    converter = _get_converter(html_content)
    result = converter.process()
    return converter.get_res(), result


if __name__ == "__main__":
    test_prepare_conf()
    html_file = Path("./demos/paragram_simple.html")
    print(html2json_process(html_file))
    print(html2json_process("<html><body><div>test</div></body></html>"))
