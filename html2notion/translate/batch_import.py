import asyncio
import aiohttp
from tqdm import tqdm
import sys
from pathlib import Path
from ..translate.notion_import import NotionImporter
from ..utils import logger


class BatchImport:
    def __init__(self, directory: Path, concurrent_limit: int = 10):
        self.directory = directory
        self.concurrent_limit = concurrent_limit

    @staticmethod
    def print_above(message):
        sys.stdout.write('\033[1A')  # Move cursor up one lines
        sys.stdout.write('\033[K')   # Clear current line
        sys.stdout.write('\r')   # Clear current line
        sys.stdout.write(message + '\n')

    @staticmethod
    async def process_file(session, file_path, pbar):
        logger.info(f"Begin file, file {file_path}")
        notion_import = NotionImporter(session)
        if file_path.is_file():
            response = await notion_import.process_file(file_path)
            BatchImport.print_above(f"Processed {file_path}")
            logger.info(f"Finish file {file_path}")
            pbar.update(1)
            return response

    async def process_directory(self):
        semaphore = asyncio.Semaphore(self.concurrent_limit)
        files_len = len(list(self.directory.glob('*')))
        pbar = tqdm(total=files_len, bar_format='{l_bar}{bar}|{n_fmt}/{total_fmt}', dynamic_ncols=True)
        print("")  # Keep a placeholder row
        BatchImport.print_above("Begin...")

        async def process_file_with_semaphore(session, file_path, pbar):
            async with semaphore:
                return await self.process_file(session, file_path, pbar)

        async with aiohttp.ClientSession() as session:
            tasks = [
                process_file_with_semaphore(session, file_path, pbar)
                for file_path in self.directory.iterdir()
                if file_path.is_file()
            ]
            results = await asyncio.gather(*tasks)
            await session.close()
            return results

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.process_directory())


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
        batch_import.run()
