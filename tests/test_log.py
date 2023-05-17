import logging
from unittest.mock import patch, MagicMock
from pathlib import Path
from html2notion.utils import setup_logger, logger
from html2notion.utils.log import CustomFormatter


class MockHandler(MagicMock):
    @property
    def level(self):
        return 0


@patch('logging.handlers.TimedRotatingFileHandler', new_callable=MockHandler)
def test_setup_logger(mock_handler):
    setup_logger(Path('/fake/path'))

    # Assert TimedRotatingFileHandler is called with the correct arguments
    mock_handler.assert_called_once_with(
        filename=Path('/fake/path', 'html2notion_error.log'),
        when='midnight', backupCount=30, encoding='utf-8'
    )

    # Assert the mock handler instance is set with the correct level and formatter
    mock_handler.return_value.setLevel.assert_called_once_with(logging.DEBUG)
    assert isinstance(mock_handler.return_value.setFormatter.call_args[0][0], CustomFormatter)

    # Assert logger has the correct level
    assert logger.level == logging.DEBUG


def test_custom_formatter():
    formatter = CustomFormatter()

    for level, color in [(logging.DEBUG, "\033[92m"), (logging.INFO, "\x1b[38;21m"),
                         (logging.WARNING, "\x1b[33;21m"), (logging.ERROR, "\x1b[31;21m"),
                         (logging.CRITICAL, "\x1b[31;1m")]:
        record = logging.LogRecord(
            name="test", level=level, pathname='test_path', lineno=0,
            msg="test message", args=None, exc_info=None
        )
        record.filename = "test.py"
        record.lineno = 1

        result = formatter.format(record)
        expected_format = f"{color}%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s\x1b[0m"
        expected_message = logging.Formatter(expected_format).format(record)

        assert result == expected_message
