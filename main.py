import argparse

from .utils import logger, config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='test/test.html', help='single html file')
    args = parser.parse_args()
    print(args.file)
    print(config['notion']['database_id'])
    logger.info(args.file)


if __name__ == '__main__':
    main()
