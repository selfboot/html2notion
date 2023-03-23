from notion_client import Client
from ..utils import logger, test_prepare_conf, config
import json


class NotionExporter:
    # Remove keys which not used by add page
    delete_conf = {
        # "object": "block",
        "id": "__any__",
        "parent": "__any__",
        "created_time": "__any__",
        "last_edited_time": "__any__",
        "created_by": "__any__",
        "last_edited_by": "__any__",
        "has_children": False,
        "archived": False,
        # "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    # "type": "text",
                    "text": {
                        # "content": "测试第一行",
                        "link": None
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    # "plain_text": "测试第一行",
                    "href": None
                }
            ],
            "color": "default"
        }
    }

    def __init__(self, api_key, page_id, page_size=2):
        self.notion = Client(auth=api_key)
        self.page_id = page_id
        self.page_size = page_size
        self.all_blocks = []
        self.output_blocks = []

    @staticmethod
    def get_delete_conf(key_path):
        result = NotionExporter.delete_conf.copy()
        for key in key_path:
            # Number in path is json array placeholder
            if isinstance(key, int):
                if isinstance(result, list) and len(result) > 0:
                    result = result[0]  # type: ignore
                else:
                    result = None
            elif isinstance(result, dict) and key in result:
                # If prefix path has __any__ conf, then delete all children
                if result[key] == "__any__":
                    return ["__any__"]
                else:
                    result = result[key]
            else:
                result = None

        if (isinstance(result, list)):
            return result
        elif (isinstance(result, str) or isinstance(result, bool) or isinstance(result, int)):
            return [result]
        else:
            return [None]

    @staticmethod
    def check_is_delete(key_path: list, value):
        delete_values = NotionExporter.get_delete_conf(key_path)
        if value in delete_values or '__any__' in delete_values:
            return True
        # logger.debug(f"Check key: {key_path}, value: {value}, delete values: {delete_values}")
        return False

    @staticmethod
    def keep_dict_pathvalue(data, path, value):
        for i, key in enumerate(path):
            if isinstance(key, int):
                data = data[key]
            elif i == len(path) - 1:
                data[key] = value
            else:
                next_key = path[i+1] if i+1 < len(path) else None
                if key in data:
                    if isinstance(next_key, int):
                        if not isinstance(data[key], list):
                            logger.error(f"Keep error: {i}, {path}, {data[key]}")
                            return
                        data[key].extend([{} for _ in range(next_key - len(data[key]) + 1)])
                    else:
                        if not isinstance(data[key], dict):
                            logger.error(f"Keep error: {i}, {path}, {data[key]}")
                            return
                else:
                    if isinstance(next_key, int):
                        data[key] = [{} for _ in range(next_key + 1)]
                    else:
                        data[key] = {}

                data = data[key]
        return

    def __get_children_blocks(self):
        children = self.notion.blocks.children.list(block_id=self.page_id, page_size=self.page_size)
        if not isinstance(children, dict):
            logger.error(f"Get children failed: {children}")
            return None

        loop_count = 1
        while isinstance(children, dict) and "has_more" in children and children["has_more"]:
            next_cursor = children["next_cursor"]
            self.all_blocks.extend(children["results"])
            children = self.notion.blocks.children.list(
                block_id=self.page_id, page_size=self.page_size, start_cursor=next_cursor)
            loop_count += 1
            cur_content = json.dumps(children, indent=4, ensure_ascii=False)
            logger.debug(f'Get child, {loop_count}: {cur_content}')

        if isinstance(children, dict) and "has_more" in children and not children["has_more"]:
            self.all_blocks.extend(children["results"])
        return children

    @staticmethod
    def export_dict(data):
        clean_block = {}
        stack = [(data, list())]
        while stack:
            cur, prefix = stack.pop()
            if isinstance(cur, dict):
                for k, v in cur.items():
                    prefix.append(k)
                    # logger.debug(f"Export dict, prefix: {prefix}, value: {v}")
                    stack.append((v, prefix[:]))
                    prefix.pop()
            elif isinstance(cur, list):
                for i, v in enumerate(cur):
                    # logger.debug(f"Export array, prefix: {prefix}, {i}, value: {v}")
                    prefix.append(i)
                    stack.append((v, prefix[:]))
                    prefix.pop()
            else:
                if (not NotionExporter.check_is_delete(prefix[:], cur)):
                    logger.debug(f"Keep {prefix}: {cur}")
                    NotionExporter.keep_dict_pathvalue(clean_block, prefix, cur)
        return clean_block

    def export_blocks(self):
        self.__get_children_blocks()
        result = json.dumps(self.all_blocks, indent=4, ensure_ascii=False)
        logger.info(f"Before process, blocks {result}")

        if not self.all_blocks:
            logger.error("Get children empty")

        for block in self.all_blocks:
            output_block = self.export_dict(block)
            self.output_blocks.append(output_block)

        return self.output_blocks
        # return json.dumps(self.all_blocks, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    test_prepare_conf()
    print(config)
    exporter = NotionExporter(api_key=config['notion']['api_key'],
                              page_id=config['notion']['page_id'],
                              page_size=10)
    exporter.export_blocks()
    print(json.dumps(exporter.output_blocks, indent=4, ensure_ascii=False))

    # testData = {
    #     "object": "block",
    #     "id": "95948188-43cb-451f-b538-e0375368ca96",
    #     "parent": {
    #         "type": "page_id",
    #         "page_id": "6d45ea01-5ba4-4ccc-a3b1-386958e2f3a7"
    #     },
    #     "created_time": "2023-03-16T12:41:00.000Z",
    #     "last_edited_time": "2023-03-16T12:41:00.000Z",
    #     "created_by": {
    #         "object": "user",
    #         "id": "6244005a-4cd8-4819-bde8-eba3de5c4cec"
    #     },
    #     "last_edited_by": {
    #         "object": "user",
    #         "id": "6244005a-4cd8-4819-bde8-eba3de5c4cec"
    #     },
    #     "has_children": False,
    #     "archived": False,
    #     "type": "paragraph",
    #     "paragraph": {
    #         "rich_text": [
    #             {
    #                 "type": "text",
    #                 "text": {
    #                     "content": "测试文本内容第3行",
    #                     "link": None
    #                 },
    #                 "annotations": {
    #                     "bold": True,
    #                     "italic": False,
    #                     "strikethrough": False,
    #                     "underline": False,
    #                     "code": False,
    #                     "color": "default"
    #                 },
    #                 "plain_text": "测试文本内容第3行",
    #                 "href": None
    #             }
    #         ],
    #         "color": "default"
    #     }
    # }

    # print(NotionExporter.check_is_delete(["outer_key"], "nested_value"))
    # print(NotionExporter.check_is_delete(["outer_key", "nested_key"], "nested_value"))
    # print(NotionExporter.check_is_delete(["outer_key", "nested_key2"], "nested_value2"))
