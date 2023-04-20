import asyncio
import pytest
import time
import os
import random
import string
from pathlib import Path
from unittest.mock import patch
from tempfile import TemporaryDirectory
from html2notion.translate.batch_import import BatchImport
from html2notion.translate.cos_uploader import TencentCosUploaderAsync
from html2notion.utils.log import log_only_local


@pytest.fixture(scope="session", autouse=True)
def prepare_conf_fixture():
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf
        test_prepare_conf()
        log_only_local("prepare_conf_fixture")


async def mock_cos_upload_request(file_path, *args, **kwargs):
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import config
        secret_id = config["cos"]["secret_id"]
        secret_key = config["cos"]["secret_key"]
        region = config["cos"]["region"]
        bucket = config["cos"]["bucket"]
    else:
        secret_id = os.environ['cos_secret_id']
        secret_key = os.environ['cos_secret_key']
        region = os.environ['cos_region']
        bucket = os.environ['cos_bucket']

    start_time = time.perf_counter()
    uploader = TencentCosUploaderAsync(secret_id, secret_key, region, bucket)
    loop = asyncio.get_event_loop()
    key = f"test_workflow/{file_path.name}"
    upload_response = await uploader.upload_file(loop, file_path, key)
    log_only_local(f"Upload response: {upload_response}")

    is_exist = await uploader.check_file_exist(loop, key)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    log_only_local(f"Upload elapsed time: {elapsed_time}")
    return (is_exist, elapsed_time)


@pytest.fixture()
def temp_dir_fixture():
    with TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        temp_files = []
        for i in range(20):
            file_size = random.randint(1 * 1024, 1 * 1024 * 1024)
            random_text = "".join(random.choices(string.ascii_letters + string.digits, k=file_size))

            temp_file = dir_path / f"file_{i}.html"
            temp_file.write_text(random_text)
            temp_files.append(temp_file)

        yield dir_path


@pytest.mark.asyncio
async def test_batch_cos_upload(temp_dir_fixture):
    concurrent_limit = 5
    dir_path = temp_dir_fixture

    start_time = time.perf_counter()
    with patch("html2notion.translate.notion_import.NotionImporter.process_file", side_effect=mock_cos_upload_request):
        batch_processor = BatchImport(
            dir_path, concurrent_limit=concurrent_limit)
        responses = await batch_processor.process_directory()
    end_time = time.perf_counter()

    for res in responses:
        assert (res[0])

    total_time = end_time - start_time
    elapsed_times = sum([res[1] for res in responses])
    least_tiems = min([res[1] for res in responses])
    log_only_local(f"Time: sum: {elapsed_times}, min {least_tiems}, total: {total_time}")
    assert (total_time < elapsed_times)
    assert (total_time >= least_tiems)
