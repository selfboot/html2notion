from aiohttp import ClientSession
from pathlib import Path
import asyncio
from ..utils import logger


class NotionImporter:
    def __init__(self, session: ClientSession):
        self.session = session

    async def fetch(self, url: str):
        async with self.session.get(url) as response:
            return await response.text()

    async def process_file(self, file_path: Path):
        with file_path.open() as f:
            content = f.read()

        logger.info(f"process file {file_path}")
        if content == "main_hold":                  # local debug
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(1)  # TODO

    @staticmethod
    def get_url_from_content(content: str):
        return content.strip()
