from html2notion.translate.notion_export import NotionExporter


def test_check_is_delete():
    del_keyvalue = [
        (["id"], "95948188-43cb-451f-b538-e0375368ca96"),
        (["parent", "type"], "page_id"),
        (["created_by", "object"], "user"),
        (["paragraph", "rich_text", 0, "text", "link"], None),
        (["paragraph", "rich_text", 0, "annotations", "code"], False),
        (["paragraph", "rich_text", 0, "annotations", "color"], "default"),
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
    ]
    for (path, value) in keep_keyvalue:
        assert not NotionExporter.check_is_delete(path, value)


if __name__ == '__main__':
    test_check_is_delete()
