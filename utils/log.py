import logging.config
import logging
from logging.handlers import TimedRotatingFileHandler
import os


class CustomFormatter(logging.Formatter):
    green = "\033[92m"
    normal = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"  # type: ignore

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


logger = logging.getLogger(__name__)
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
log_path = os.path.join(script_dir, "../logs/error.log")
handler = TimedRotatingFileHandler(filename=log_path, when='midnight', backupCount=30, encoding='utf-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug('Logging debug message')
logger.info('Logging info message')
logger.warn('Logging debug message')
logger.error('Logging error message')
