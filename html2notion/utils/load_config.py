import json
import os
import sys

config = {}


def read_config(file_path):
    if not file_path.is_file():
        print(f"Load {file_path} fail")
        sys.exit(1)

    with open(file_path, "r") as f:
        config = json.load(f)

        """
        {
            "notion": {
                "database_id": "xxxxx",
                "api_key": "xxxxx"
            }
        }
        """
        if "notion" not in config:
            raise Exception("notion is not set in config.json")

        notion_conf = config["notion"]
        if "database_id" not in notion_conf:
            raise Exception("database_id is not set in config.json")
        if "api_key" not in notion_conf:
            raise Exception("api_key is not set in config.json")

        if "log_path" not in config:
            config["log_path"] = os.path.expanduser('~/logs')
        return True
