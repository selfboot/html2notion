import asyncio
import pytest
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory
from html2notion.translate.batch_import import BatchImport
from http import HTTPStatus
import time
import os

process_once_time = 1


@pytest.fixture(scope="session", autouse=True)
def prepare_conf_fixture():
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf, logger
        test_prepare_conf()
        logger.info("prepare_conf_fixture")


async def mock_notion_api_request(file_path, *args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, file_content):
            self.status_code = status_code
            self.file_content = file_content

        def json(self):
            return {"result": "success", "file_content": self.file_content}

    content = file_path.read_text()
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import logger
        logger.debug(f"mock_notion_api_request: {file_path}")
    await asyncio.sleep(process_once_time)

    return MockResponse(HTTPStatus.OK, content)


@pytest.fixture(params=[10, 20])
def temp_dir_fixture(request):
    num_files = request.param
    with TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        temp_files = []
        for i in range(num_files):
            temp_file = dir_path / f"file{i}.txt"
            temp_file.write_text(f"file{i}")
            temp_files.append(temp_file)

        yield dir_path


@pytest.mark.parametrize("concurrent_limit", [1, 5, 10])
@pytest.mark.asyncio
async def test_batch_process(temp_dir_fixture, concurrent_limit):
    dir_path = temp_dir_fixture
    start_time = time.time()
    with patch("html2notion.translate.notion_import.NotionImporter.process_file", side_effect=mock_notion_api_request) as mock_process_file:
        batch_processor = BatchImport(dir_path, concurrent_limit=concurrent_limit)
        responses = await batch_processor.process_directory()

    end_time = time.time()
    for file_path, response in zip(
            sorted(dir_path.iterdir()),
            sorted(responses, key=lambda x: x.json()["file_content"])):
        assert response.json()["file_content"] == f"{file_path.stem}"

    total_time = end_time - start_time
    expected_time = max(len(list(dir_path.iterdir())) / concurrent_limit, process_once_time)
    schedule_more_time = 1.5
    assert total_time >= expected_time
    assert total_time <= expected_time * 1.5
