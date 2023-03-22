import json
import sys
from pathlib import Path

config = {}


def read_config(file_path):
    """
    {
        "notion": {
            "database_id": "xxxxx",
            "api_key": "xxxxx"
        }
    }
    """
    if not file_path.is_file():
        print(f"Load {file_path} fail")
        sys.exit(1)

    with open(file_path, "r") as f:
        json_conf = json.load(f)

    config.update(json_conf)
    if "notion" not in config:
        raise Exception("notion is not set in config.json")

    notion_conf = config["notion"]
    if "database_id" not in notion_conf:
        raise Exception("database_id is not set in config.json")
    if "api_key" not in notion_conf:
        raise Exception("api_key is not set in config.json")

    if "log_path" not in config:
        config["log_path"] = Path('~/logs')
    return
