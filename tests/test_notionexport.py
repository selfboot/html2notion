from html2notion.translate.notion_export import NotionExporter
import os
import json


def test_check_is_delete():
    del_keyvalue = [
        (["id"], "95948188-43cb-451f-b538-e0375368ca96"),
        (["parent", "type"], "page_id"),
        (["created_by", "object"], "user"),
        (["paragraph", "rich_text", 0, "text", "link"], None),
        (["paragraph", "rich_text", 0, "annotations", "code"], False),
        (["paragraph", "rich_text", 0, "annotations", "color"], "default"),
        (["quote", "rich_text", 0, "annotations", "color"], "default"),
        (["numbered_list_item", "rich_text", 0, "annotations", "color"], "default"),
        (["bulleted_list_item", "rich_text", 0, "annotations", "color"], "default"),
    ]

    for (path, value) in del_keyvalue:
        assert NotionExporter.check_is_delete(path, value)

    keep_keyvalue = [
        (["type"], "paragraph"),
        (["type"], "image"),
        (["object"], "block"),
        (["paragraph", "rich_text", 0, "text", "link"], "https://selfboot.com"),
        (["paragraph", "rich_text", 0, "annotations", "code"], True),
        (["paragraph", "rich_text", 0, "annotations", "color"], "red"),
        (["quote", "rich_text", 0, "annotations", "color"], "red"),
        (["numbered_list_item", "rich_text", 0, "annotations", "color"], "red"),
        (["bulleted_list_item", "rich_text", 0, "annotations", "color"], "red"),
        (["bulleted_list_item", "rich_text", 0, "annotations", "code"], True),
    ]
    for (path, value) in keep_keyvalue:
        assert not NotionExporter.check_is_delete(path, value)


def test_export_blocks():
    if 'GITHUB_ACTIONS' in os.environ:
        api_key = os.environ['notion_api_key']
        page_id = os.environ['notion_page_id_1']
    else:
        from html2notion.utils import config, test_prepare_conf
        test_prepare_conf()
        api_key = config['notion']['api_key']
        page_id = config['notion']['page_id']

    names = locals()
    page_sizes = [1, 5, 10, 100]
    for i in page_sizes:
        names['exporter_' + str(i)] = NotionExporter(
            api_key=api_key,
            page_id=page_id,
            page_size=i)

        names['exporter_' + str(i)].export_blocks()
        names['page_json_'+str(i)] = json.dumps(names['exporter_' + str(i)].output_blocks, indent=4, ensure_ascii=False)

    for i in page_sizes[1:]:
        if names['page_json_' + str(i)] != names['page_json_' + str(page_sizes[0])]:
            assert False


if __name__ == '__main__':
    if 'GITHUB_ACTIONS' not in os.environ:
        from html2notion.utils import config, test_prepare_conf
        test_prepare_conf()

    test_check_is_delete()
    test_export_blocks()
