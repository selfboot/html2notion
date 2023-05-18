import asyncio
import pytest
import time
import os
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory
from http import HTTPStatus
from html2notion.translate.batch_import import BatchImport
from html2notion.utils import rate_limit
from html2notion.utils.log import log_only_local

process_once_time = 0.5


async def mock_notion_api_request(file_path, *args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, file_content, elapsed_time):
            self.status_code = status_code
            self.file_content = file_content
            self.elapsed_time = elapsed_time

        def json(self):
            return {"result": "success", "file_content": self.file_content, "elapsed_time": self.elapsed_time}

    start_time = time.perf_counter()
    content = file_path.read_text()
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import logger
        logger.debug(f"mock_notion_api_request: {file_path}")
    await asyncio.sleep(process_once_time)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return MockResponse(HTTPStatus.OK, content, elapsed_time)


async def mock_notion_create_page(notion_data, *args, **kwargs):
    async with rate_limit:
        await asyncio.sleep(0.01)
        log_only_local(f"mock_notion_create_page")
    return "succ"

@pytest.fixture(params=[10, 20])
def temp_dir_fixture(request):
    num_files = request.param
    with TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        temp_files = []
        for i in range(num_files):
            temp_file = dir_path / f"file{i}.html"
            temp_file.write_text(f"file{i}")
            temp_files.append(temp_file)

        yield dir_path


@pytest.mark.parametrize("concurrent_limit", [2, 5, 10])
@pytest.mark.asyncio
async def test_batch_process(temp_dir_fixture, concurrent_limit):
    dir_path = temp_dir_fixture
    start_time = time.perf_counter()
    with patch("html2notion.translate.notion_import.NotionImporter.process_file", side_effect=mock_notion_api_request):
        batch_processor = BatchImport(
            dir_path, concurrent_limit=concurrent_limit)
        responses = await batch_processor.process_directory()

    end_time = time.perf_counter()
    for file_path, response in zip(
            sorted(dir_path.iterdir()),
            sorted(responses, key=lambda x: x.json()["file_content"])):
        assert response.json()["file_content"] == f"{file_path.stem}"

    total_time = end_time-start_time
    sync_time = sum(res.json()["elapsed_time"] for res in responses)
    least_time = min(res.json()["elapsed_time"] for res in responses)
    log_only_local(
        f"total_time: {total_time}, sync_time: {sync_time}, least_time: {least_time}")
    assert total_time >= least_time
    assert total_time <= sync_time


@pytest.mark.parametrize("concurrent_limit", [5, 10, 20])
@pytest.mark.asyncio
async def test_reqlimit(temp_dir_fixture, concurrent_limit):
    dir_path = temp_dir_fixture
    start_time = time.perf_counter()
    with patch("html2notion.translate.notion_import.NotionImporter.create_new_page", side_effect=mock_notion_create_page):
        batch_processor = BatchImport(dir_path, concurrent_limit=concurrent_limit)
        responses = await batch_processor.process_directory()

    end_time = time.perf_counter()
    total_time = end_time-start_time
    num_files = len(list(dir_path.glob('*.html')))
    log_only_local(f"file nums: {num_files}, concurrent {concurrent_limit}, total_time: {total_time}")
    # The time deviation within 1 second is acceptable here.
    assert (total_time >= num_files / 3 - 1)