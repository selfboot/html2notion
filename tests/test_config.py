import pytest
from pathlib import Path
from unittest.mock import mock_open, patch
from html2notion.utils import read_config, config
import pytest


def test_read_config():
    mock_file_content = """{
    "notion": {
        "database_id": "test_db_id",
        "api_key": "test_api_key"
    },
    "log_path": "/test/log/path"
    }
    """
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch.object(Path, "is_file", return_value=True):
            read_config(Path("test_config.json"))
            assert "notion" in config
            assert "database_id" in config["notion"]
            assert "api_key" in config["notion"]
            assert config["notion"]["database_id"] == "test_db_id"
            assert config["notion"]["api_key"] == "test_api_key"
            config.clear()

    # Testing for missing database_id, notion, or api_key configurations throws an exception
    with patch("builtins.open", mock_open(read_data="{}")), patch.object(Path, "is_file", return_value=True), pytest.raises(Exception, match="notion is not set in config.json"):
        read_config(Path("test_config.json"))
        config.clear()

    with patch("builtins.open", mock_open(read_data="{\"notion\": {}}")), patch.object(Path, "is_file", return_value=True), pytest.raises(Exception, match="database_id is not set in config.json"):
        read_config(Path("test_config.json"))
        config.clear()

    with patch("builtins.open", mock_open(read_data="{\"notion\": {\"database_id\": \"test_db_id\"}}")), patch.object(Path, "is_file", return_value=True), pytest.raises(Exception, match="api_key is not set in config.json"):
        read_config(Path("test_config.json"))
        config.clear()
