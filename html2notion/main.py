import argparse
import os
import sys
from pathlib import Path
import asyncio
from aiohttp import ClientSession
from notion_client import AsyncClient
from .utils import setup_logger, read_config, logger, config
from .translate.notion_import import NotionImporter
from .translate.batch_import import BatchImport


def parse_args():
    parser = argparse.ArgumentParser(
        description='Html2notion: Save HTML to your Notion notes quickly and easily, while keeping the original format as much as possible')
    parser.add_argument('--conf', type=str, help='conf file path', required=True)
    parser.add_argument('--log', type=str, help='log direct path')
    parser.add_argument('--batch', type=int, default=15, help='batch save concurrent limit')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help='Save single html file to notion')
    group.add_argument('--dir', type=str, help='Save all html files in the dir to notion')
    return parser.parse_args()


def prepare_env(args: argparse.Namespace):
    log_path = Path(args.log) if args.log else Path.cwd() / 'logs/'
    if not log_path.is_dir():
        log_path.mkdir(parents=True)

    conf_path = Path(args.conf)
    if not conf_path.is_file():
        print(f"Read conf file({conf_path}) failed.")
        logger.fatal(f"Read conf file({conf_path}) failed.")
        sys.exit(1)

    setup_logger(log_path)
    read_config(conf_path)
    logger.info(f"Read log {log_path}, conf {conf_path}")


async def import_single_file(file):
    notion_api_key = ""
    if 'GITHUB_ACTIONS' in os.environ:
        notion_api_key = os.environ['notion_api_key']
    else:
        notion_api_key = config['notion']['api_key']
    async with ClientSession() as session:
        async with AsyncClient(auth=notion_api_key) as notion_client:
            notion_importer = NotionImporter(session, notion_client)
            result = await notion_importer.process_file(file)
            return result


def main():
    args = parse_args()
    prepare_env(args)

    file_path = Path(args.file) if args.file else None
    dir_path = Path(args.dir) if args.dir else None
    max_concurrency = args.batch
    if file_path and file_path.is_file():
        logger.info(f"Begin save single html file: {file_path}.")
        result = asyncio.run(import_single_file(file_path))
        logger.info(f"Finish save single html file: {file_path}.\n{result}")
        print(f"File {file_path} saved.")
    elif dir_path and dir_path.is_dir():
        logger.info(f"Begin save all html files in the dir: {dir_path}.")
        batch_import = BatchImport(dir_path, max_concurrency)
        result = asyncio.run(batch_import.process_directory())
        logger.info(f"Finish save all html files in the dir: {dir_path}.\n{result}")
        print(f"Directory {dir_path} saved.")
    else:
        print("No impossible.")
    return


if __name__ == '__main__':
    main()
