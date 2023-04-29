import asyncio
import os
from aiohttp import ClientSession
from pathlib import Path
from notion_client import AsyncClient
from notion_client.errors import RequestTimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from ..utils import logger, test_prepare_conf, config, rate_limit
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

        create_result = await self.create_new_page(notion_data)
        logger.info(f"Create notion page: {create_result}")
        return "succ"

    # https://developers.notion.com/reference/request-limits
    # The rate limit for incoming requests per integration is an average of three requests per second. 
    # Doc of create page: https://developers.notion.com/reference/post-page
    @retry(stop=stop_after_attempt(5),
           wait=wait_exponential(multiplier=1, min=3, max=30),
           retry=retry_if_exception_type(RequestTimeoutError))
    async def create_new_page(self, notion_data):
        # logger.debug(f'Create new page: {notion_data["parent"]}, {notion_data["properties"]}')
        # body.children.length should be ≤ `100`,
        blocks = notion_data.get("children", [])
        limit_size = 100
        chunks = [blocks[i: i + limit_size] for i in range(0, len(blocks), limit_size)]
        if blocks:
            notion_data.pop("children")
        first_chunk = chunks[0] if chunks else []
        async with rate_limit:
            created_page = await self.notion_client.pages.create(**notion_data, children=first_chunk)
            page_id = created_page["id"]
            for chunk in chunks[1:]:
                await self.notion_client.blocks.children.append(page_id, children=chunk)
        return created_page


async def main(file_path, notion_api_key):
    async with ClientSession() as session:
        async with AsyncClient(auth=notion_api_key) as notion_client:
            importer = NotionImporter(session, notion_client)
            result = await importer.process_file(file_path)
            logger.info(f"Import result: {result}")


if __name__ == "__main__":
    test_prepare_conf()
    file = Path("./demos/Test Case E.html")
    notion_api_key = ""
    if 'GITHUB_ACTIONS' in os.environ:
        notion_api_key = os.environ['notion_api_key']
    else:
        notion_api_key = config['notion']['api_key']
    asyncio.run(main(file, notion_api_key))
