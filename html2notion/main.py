import argparse
from pathlib import Path
from .utils import setup_logger, read_config, logger


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

    print(f"Read {log_path} {conf_path}")
    logger.info(f"Read {log_path} {conf_path}")


if __name__ == '__main__':
    main()
