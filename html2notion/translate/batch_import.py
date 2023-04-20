import asyncio
import aiohttp
import os
import shutil
import sys
from tqdm import tqdm
from pathlib import Path
from notion_client import AsyncClient
from ..translate.notion_import import NotionImporter
from ..utils import logger, config


class BatchImport:
    def __init__(self, directory: Path, concurrent_limit: int = 10):
        self.directory = directory
        self.concurrent_limit = concurrent_limit
        if 'GITHUB_ACTIONS' in os.environ:
            self.notion_api_key = os.environ['notion_api_key']
        else:
            self.notion_api_key = config['notion']['api_key']
        self.notion_client = AsyncClient(auth=self.notion_api_key)

    @staticmethod
    def print_above(message):
        term_width, _ = shutil.get_terminal_size()
        sys.stdout.write('\033[1A')  # Move cursor up one line
        sys.stdout.write('\r')       # Reset cursor position to the beginning of the line
        sys.stdout.write(' ' * term_width)  # Fill the entire line with spaces
        sys.stdout.write('\r')       # Reset cursor position to the beginning of the line again
        sys.stdout.write(message + '\n')

    @staticmethod
    async def process_file(session, notion_client, file_path, pbar):
        logger.info(f"Begin file, file {file_path}")
        notion_import = NotionImporter(session, notion_client)
        if file_path.is_file():
            response = await notion_import.process_file(file_path)
            BatchImport.print_above(f"Processed {file_path}")
            logger.info(f"Finish file {file_path}")
            pbar.update(1)
            return response

    async def process_directory(self):
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        html_files = [file_path for file_path in self.directory.glob('*.html') if file_path.name != 'index.html']
        files_len = len(html_files)
        pbar = tqdm(total=files_len, bar_format='{l_bar}{bar}|{n_fmt}/{total_fmt}', dynamic_ncols=True)
        print("")  # Keep a placeholder row
        BatchImport.print_above("Begin...")

        async def process_file_with_semaphore(session, notion_client, file_path, pbar):
            async with semaphore:
                return await self.process_file(session, notion_client, file_path, pbar)

        async with aiohttp.ClientSession() as session:
            tasks = [
                process_file_with_semaphore(session, self.notion_client, file_path, pbar)
                for file_path in html_files
            ]
            results = await asyncio.gather(*tasks)
            await session.close()
            return results


if __name__ == '__main__':
    from ..utils import test_prepare_conf
    test_prepare_conf()
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        files = []
        for i in range(100):
            temp_file = temp_dir_path / f"file{i}.txt"
            temp_file.write_text("main_hold")
            files.append(temp_file)

        max_concurrency = 2
        batch_import = BatchImport(temp_dir_path, max_concurrency)
        result = asyncio.run(batch_import.process_directory())
        print(result)
