import logging
from logging import handlers
import os
logger = logging.getLogger()


class CustomFormatter(logging.Formatter):
    green = "\033[92m"
    normal = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # type: ignore
    format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"

    FORMATS = {
        logging.DEBUG: green + format + reset,  # type: ignore
        logging.INFO: normal + format + reset,  # type: ignore
        logging.WARNING: yellow + format + reset,  # type: ignore
        logging.ERROR: red + format + reset,  # type: ignore
        logging.CRITICAL: bold_red + format + reset  # type: ignore
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logger(log_path):
    filename = os.path.join(log_path.resolve(), "html2notion_error.log")
    handler = handlers.TimedRotatingFileHandler(
        filename=filename, when='midnight', backupCount=30, encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    logger.debug('Logging debug message')
    logger.info('Logging info message')
    logger.warn('Logging debug message')
    logger.error('Logging error message')
