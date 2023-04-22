import asyncio
import aiohttp
import os
from pathlib import Path
from asyncio import Lock
from notion_client import AsyncClient
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
)
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
        self.all_files = []
        self.failed_files = []
        self.success_files = []
        self.files_lock = Lock()

    @staticmethod
    async def process_file(session, notion_client, file_path, files_lock, failed_files, success_files):
        logger.info(f"Begin file, file {file_path}")
        notion_import = NotionImporter(session, notion_client)
        if file_path.is_file():
            try:
                response = await notion_import.process_file(file_path)
                logger.info(f"Finish file {file_path}")
                async with files_lock:
                    success_files.append(file_path)
                return response
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                async with files_lock:
                    failed_files.append((file_path, str(e)))
                return None
        else:
            logger.error(f"Error processing {file_path}: File not found")
            async with files_lock:
                    failed_files.append((file_path, "File not found"))
            return None

    async def process_directory(self):
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        self.all_files = [file_path for file_path in self.directory.glob('*.html') if file_path.name != 'index.html']
        files_len = len(self.all_files)

        with Progress(
            TextColumn("[progress.description]{task.description}", justify="right"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn(" "),
            TimeRemainingColumn()
        ) as progress:
            # with Progress() as progress:
            progress.add_task("[cyan]Total", total=files_len,
                              completed=files_len, update_period=0, style="cyan")
            success_task_id = progress.add_task(
                "[green]Success", total=files_len, style="green")
            failed_task_id = progress.add_task("[red]Failed", total=files_len, style="red")
            async def process_file_with_semaphore(session, notion_client, file_path):
                async with semaphore:
                    result = await self.process_file(session, notion_client, file_path, self.files_lock, self.failed_files, self.success_files)
                    if result:
                        progress.update(success_task_id, advance=1)
                    else:
                        progress.update(failed_task_id, advance=1)
                    return result

            async with aiohttp.ClientSession() as session:
                tasks = [process_file_with_semaphore(session, self.notion_client, file_path) for file_path in self.all_files]
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
