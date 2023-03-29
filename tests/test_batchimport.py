import pytest
from aiohttp import web
from pathlib import Path
from tempfile import TemporaryDirectory
import asyncio
from html2notion.translate.batch_import import BatchImport


@pytest.fixture(scope="session", autouse=True)
def prepare_conf_fixture():
    import os
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import test_prepare_conf, logger
        test_prepare_conf()
        logger.info("prepare_conf_fixture")


@pytest.fixture
def url_server_fixture():
    async def serve_url(request):
        await asyncio.sleep(0.5)  # Simulate network latency
        return web.Response(text="Hello, world!")

    app = web.Application()
    app.router.add_get("/", serve_url)

    runner = web.AppRunner(app)
    yield runner
    asyncio.run(runner.cleanup())


def get_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture
async def url_server(url_server_fixture):
    await url_server_fixture.setup()
    port = get_free_port()
    site = web.TCPSite(url_server_fixture, "localhost", port)
    await site.start()
    yield site, port
    await site.stop()


@pytest.fixture
async def port_fixture(url_server):
    _, port = url_server
    return port


@pytest.fixture(params=[5, 20])
def temp_dir_fixture(port_fixture, request):
    port = port_fixture
    num_files = request.param
    with TemporaryDirectory() as temp_dir:
        dir_path = Path(temp_dir)
        temp_files = []
        for i in range(num_files):
            temp_file = dir_path / f"file{i}.txt"
            temp_file.write_text(f"http://localhost:{port}")
            temp_files.append(temp_file)

        yield dir_path


@pytest.mark.parametrize("concurrent_limit", [1, 5, 10])
@pytest.mark.asyncio
async def test_batch_process(url_server, temp_dir_fixture, concurrent_limit):
    dir_path = temp_dir_fixture
    batch_processor = BatchImport(dir_path, concurrent_limit=concurrent_limit)
    await batch_processor.process_directory()
