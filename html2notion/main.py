import argparse
import os
import sys
import asyncio
from pathlib import Path
from aiohttp import ClientSession
from notion_client import AsyncClient
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from .utils import setup_logger, read_config, logger, config
from .translate.notion_import import NotionImporter
from .translate.batch_import import BatchImport
from .translate.import_stats import StatLevel
console = Console()


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


def print_single_stats(stat):
    if stat.get_level() == StatLevel.EXCEPTION.value:
        text = Text(f"Failed to import {stat.filename}", style="default")
        text.append(f"\nException: {stat.exception}", style="red")
        console.print(text)
        return
    
    title = f"{stat.filename}" if stat.filename else "Import Result (Loss filename)"
    style = "default"
    if stat.get_level() == StatLevel.LOSS.value:
        title += " (Loss some content)"
        style = "yellow"
    elif stat.get_level() == StatLevel.SUCC.value:
        title += "(Import successfully)"
        style = "green"
        
    table = Table(title=title, title_style=style, expand=True, box=box.HEAVY_HEAD, show_lines=True)
    table.add_column("Item", justify="right", style="default")
    table.add_column("Html", style="default")
    table.add_column("Notion", justify="left", style="default")
    table.add_row("Text Len", str(stat.text_count), str(stat.notion_text_count))
    table.add_row("Image Count", str(stat.image_count), str(stat.notion_image_count))
    if stat.skip_tag:
        table.add_row("Skip Tag Count", "", 'Detail: [yellow]' + ";".join([repr(s)
                      for s in stat.skip_tag])[:2000] + "[/yellow]")
 
    console.print(table)


def print_batch_stats(batch_import):
    all_files = batch_import.all_files
    batch_stats = batch_import.batch_stats
    success_stats = [stat for stat in batch_stats if not stat.get_level() == StatLevel.SUCC.value]
    if len(success_stats) == len(all_files):
        console.print(f"All files migrated successfully and there is no data loss.", style="green")

    failed_stats = [stat for stat in batch_stats if stat.get_level() == StatLevel.EXCEPTION.value]
    if failed_stats:
        table = Table(title=f"\nImport Fail Exception Detail\nLog path: {config.get('log_path')}", expand=True, box=box.HEAVY_HEAD, show_lines=True)
        table.add_column("File Name", justify="left", style="default")
        table.add_column("Fail Reason", justify="left", style="default")

        for stat in failed_stats:
            table.add_row(str(stat.filename), str(stat))
        console.print(table)

    less_stats = [stat for stat in batch_stats if stat.get_level() == StatLevel.LOSS.value]
    if less_stats:
        table = Table(title=f"\nImport Data Loss Detail (You can use --file to import single file for more info)\n", expand=True, box=box.HEAVY_HEAD, show_lines=True)
        table.add_column("File Name", justify="left", style="default")
        table.add_column("Loss Detail", justify="left", style="default")

        for stat in less_stats:
            table.add_row(str(stat.filename), str(stat))
        console.print(table)



def prepare_env(args: argparse.Namespace):
    log_path = Path(args.log) if args.log else Path.cwd() / 'logs/'
    if not log_path.is_dir():
        log_path.mkdir(parents=True)

    conf_path = Path(args.conf)
    if not conf_path.is_file():
        console.print(f"Read conf file({conf_path}) failed.", style="red")
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
            await notion_importer.process_file(file)
            return notion_importer.import_stats


def main():
    args = parse_args()
    prepare_env(args)

    file_path = Path(args.file) if args.file else None
    dir_path = Path(args.dir) if args.dir else None
    max_concurrency = args.batch
    if file_path and file_path.is_file():
        stats = asyncio.run(import_single_file(file_path))
        print_single_stats(stats)
    elif dir_path and dir_path.is_dir():
        logger.info(f"Begin save all html files in the dir: {dir_path}.")
        batch_import = BatchImport(dir_path, max_concurrency)
        result = asyncio.run(batch_import.process_directory())
        logger.info(f"Finish save all html files in the dir: {dir_path}.\n{result}")
        print_batch_stats(batch_import)
    else:
        text = Text("The parameters provided are incorrect, please check.", style="red")

    text = Text("\nIf you need help, please submit an ", style="default")
    link = Text("issue", style="cyan underline link https://github.com/selfboot/html2notion/issues")
    text.append(link)
    text.append(" on gitHub.", style="default")
    console.print(text)
    return


if __name__ == '__main__':
    main()
