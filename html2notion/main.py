import argparse
import sys
import json
from pathlib import Path
from .utils import setup_logger, read_config, logger
from .translate.html2json import Html2Json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--html', type=str, default='test.html',
                        help='html file to convert')
    parser.add_argument('--conf', type=str, default='./config.json',
                        help='conf file path', required=True)
    parser.add_argument('--log', type=str, default='~/logs',
                        help='log direct path', required=True)

    args = parser.parse_args()
    log_path = Path(args.log)
    conf_path = Path(args.conf)
    setup_logger(log_path)
    read_config(conf_path)

    html_path = Path(args.html)
    if html_path.is_file():
        logger.info(f"Read html file({html_path}).")
        html2json = Html2Json(html_path)
        html2json.convert()
        print(json.dumps(html2json.children, indent=4, ensure_ascii=False))

    else:
        print(f"Read html file({html_path}) failed.")
        logger.fatal(f"Read html file({html_path}) failed.")
        sys.exit(1)

    logger.info(f"Read log path({log_path}), conf path({conf_path})")


if __name__ == '__main__':
    main()
