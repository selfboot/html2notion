from bs4 import BeautifulSoup


def convert_html_to_json(html, tag_mapping=None):
    """
    Convert HTML to a JSON object.

    :param html: str, the HTML code to be converted
    :param tag_mapping: dict, a dictionary that maps HTML tags to JSON objects
    :return: dict, the converted JSON object
    """
    soup = BeautifulSoup(html, 'html.parser')
    rich_text = []
    if not tag_mapping:
        tag_mapping = {
            'div': {'type': 'paragraph'},
            'span': {'type': 'text'},
            'b': {'annotations': {'bold': True}},
            'i': {'annotations': {'italic': True}},
            'u': {'annotations': {'underline': True}},
            'strike': {'annotations': {'strikethrough': True}},
            'font': {'annotations': {'color': 'red'}}
        }
    for child in soup.body.children:
        if child.name in tag_mapping:
            tag_info = tag_mapping[child.name]
            if 'type' in tag_info:
                obj_type = tag_info['type']
                obj_data = {}
                if obj_type == 'paragraph':
                    obj_data['rich_text'] = convert_html_to_rich_text(child, tag_mapping)
                else:
                    obj_data['text'] = {'content': child.text}
                    if 'annotations' in tag_info:
                        obj_data['annotations'] = tag_info['annotations']
                rich_text.append({'type': obj_type, **obj_data})
    return {
        'object': 'block',
        **rich_text[0]
    }


def convert_html_to_rich_text(node, tag_mapping):
    rich_text = []
    for child in node.children:
        if child.name in tag_mapping:
            tag_info = tag_mapping[child.name]
            obj_data = {}
            if 'annotations' in tag_info:
                obj_data['annotations'] = tag_info['annotations']
            if 'type' in tag_info:
                obj_type = tag_info['type']
                if obj_type == 'text':
                    obj_data['text'] = {'content': child.text}
                    rich_text.append({'type': 'text', **obj_data})
                else:
                    obj_data['rich_text'] = convert_html_to_rich_text(child, tag_mapping)
                    rich_text.append({'type': obj_type, **obj_data})
    return rich_text
