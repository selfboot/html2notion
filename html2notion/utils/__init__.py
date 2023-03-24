from .log import logger, setup_logger
from .load_config import read_config, config
from pathlib import Path


def test_prepare_conf():
    log_path = Path("./logs")
    conf_path = Path("./.config.json")
    setup_logger(log_path)
    read_config(conf_path)
    logger.info(f"test_prepare_conf, log path({log_path}), conf path({conf_path})")


__all__ = ['logger', 'setup_logger', 'config', 'read_config', 'test_prepare_conf']
