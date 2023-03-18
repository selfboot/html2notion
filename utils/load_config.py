import json
import os
import sys
from .log import logger


def read_config(filename):
    if not os.path.exists(filename):
        print("Load config from file %s failed. ", filename)
        logger.error("Load config from file %s failed. ", filename)
        sys.exit(1)

    with open(filename, "r") as f:
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

        return config


script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
config = read_config(os.path.join(script_dir, "../config.json"))
