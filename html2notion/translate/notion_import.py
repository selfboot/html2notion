import asyncio
import os
from aiohttp import ClientSession
from pathlib import Path
from notion_client import AsyncClient
from ..utils import logger, test_prepare_conf, config
from ..translate.html2json import html2json_process


class NotionImporter:
    def __init__(self, session: ClientSession, notion_client):
        self.session = session
        self.notion_client = notion_client

    async def process_file(self, file_path: Path):
        if not file_path.is_file():
            logger.error(f"{file_path} is not a file.")
            return

        with file_path.open() as f:
            content = f.read()

        logger.info(f"Process file {file_path}")
        if content == "main_hold":                  # local debug
            await asyncio.sleep(1)
            return "main_hold"

        notion_data, html_type = html2json_process(file_path)
        logger.info(f"path: {file_path}, html type: {html_type}")

        create_result = await self.create_new_page(config['notion']['database_id'], notion_data)
        logger.info(f"Create notion page: {create_result}")
        return "succ"

    async def create_new_page(self, database_id, notion_data):
        created_page = await self.notion_client.pages.create(
            parent={"type": "database_id", "database_id": database_id},
            properties=notion_data,
        )
        return created_page


async def main(file_path, notion_api_key):
    async with ClientSession() as session:
        async with AsyncClient(auth=notion_api_key) as notion_client:
            importer = NotionImporter(session, notion_client)
            result = await importer.process_file(file_path)
            logger.info(f"Import result: {result}")


if __name__ == "__main__":
    test_prepare_conf()
    file = Path("demos/yinxiang.html")
    notion_api_key = ""
    if 'GITHUB_ACTIONS' in os.environ:
        notion_api_key = os.environ['notion_api_key']
    else:
        notion_api_key = config['notion']['api_key']
    asyncio.run(main(file, notion_api_key))
