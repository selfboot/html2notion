import pytest
import os
from html2notion.utils import test_prepare_conf, logger


@pytest.fixture(autouse=True, scope='module')
def prepare_conf():
    if 'GITHUB_ACTIONS' not in os.environ:
        test_prepare_conf()
        logger.info("prepare_conf_fixture")
