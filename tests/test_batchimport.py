import pytest
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory
from html2notion.translate.batch_import import BatchImport
from http import HTTPStatus
import time


@pytest.fixture(scope="session", autouse=True)
def prepare_conf_fixture():
    import os
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf, logger
        test_prepare_conf()
        logger.info("prepare_conf_fixture")


def mock_notion_api_request(file_path, *args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, content):
            self.status_code = status_code
            self.content = content

        def json(self):
            return {"result": "success", "content": self.content}
    content = file_path.read_text()
    from html2notion.utils import logger
    logger.info("mock_notion_api_request")
    time.sleep(1)
    return MockResponse(HTTPStatus.OK, content)


@pytest.fixture(params=[5, 20])
def temp_dir_fixture(request):
    num_files = request.param
    with TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        temp_files = []
        for i in range(num_files):
            temp_file = dir_path / f"file{i}.txt"
            temp_file.write_text(f"{i}")
            temp_files.append(temp_file)

        yield dir_path


@pytest.mark.parametrize("concurrent_limit", [1, 5, 10])
@pytest.mark.asyncio
async def test_batch_process(temp_dir_fixture, concurrent_limit):
    dir_path = temp_dir_fixture
    with patch("html2notion.translate.notion_import.NotionImporter.process_file", side_effect=mock_notion_api_request):
        batch_processor = BatchImport(dir_path, concurrent_limit=concurrent_limit)
        await batch_processor.process_directory()
