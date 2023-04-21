import re
import os
from collections import namedtuple
from enum import Enum
from ..utils import logger, config

class Block(Enum):
    FAIL = "fail"
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    NUMBERED_LIST = "numbered_list_item"
    BULLETED_LIST = "bulleted_list_item"

class Html2JsonBase:
    _registry = {}
    _text_annotations = {
        "bold": bool,
        "italic": bool,
        "strikethrough": bool,
        "underline": bool,
        "code": bool,
        "color": str,
    }

    _color_tuple = namedtuple("Color", "name r g b")
    _notion_color = [
        _color_tuple("gray", 128, 128, 128),
        _color_tuple("brown", 165, 42, 42),
        _color_tuple("orange", 255, 165, 0),
        _color_tuple("yellow", 255, 255, 0),
        _color_tuple("green", 0, 128, 0),
        _color_tuple("blue", 0, 0, 255),
        _color_tuple("purple", 128, 0, 128),
        _color_tuple("pink", 255, 192, 203),
        _color_tuple("red", 255, 0, 0),
    ]

    # Page content should be: https://developers.notion.com/reference/post-page
    def __init__(self, html_content):
        self.html_content = html_content
        self.children = []
        self.properties = {}
        self.parent = {}
        if 'GITHUB_ACTIONS' in os.environ:
            notion_database_id = os.environ['notion_db_id_1']
        else:
            notion_database_id = config['notion']['database_id']
        self.parent = {"type": "database_id", "database_id": notion_database_id}

    def process(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_notion_data(self):
        return {
            key: value
            for key, value in {
                'children': self.children,
                'properties': self.properties,
                'parent': self.parent,
            }.items()
            if value
        }

    @staticmethod
    def generate_link(**kwargs):
        if not kwargs.get("plain_text", ""):
            return
        return {
            "href": kwargs.get("url", ""),
            "plain_text": kwargs.get("plain_text", ""),
            "text": {
                "link": {"url": kwargs.get("url", "")},
                "content": kwargs.get("plain_text", "")
            },
            "type": "text"
        }

    @staticmethod
    def generate_text(**kwargs):
        plain_text = kwargs.get("plain_text", "")
        if not plain_text:
            return
        annotations = {
            key: value
            for key, value in kwargs.items()
            if key in Html2JsonBase._text_annotations and isinstance(value, Html2JsonBase._text_annotations[key])
        }
        text_obj = {
            "plain_text": plain_text,
            "text": {"content": plain_text},
            "type": "text"
        }
        if annotations:
            text_obj["annotations"] = annotations

        return text_obj

    @staticmethod
    def generate_properties(**kwargs):
        title = kwargs.get("title", "")
        url = kwargs.get("url", "")
        tags = kwargs.get("tags", [])
        created_time = kwargs.get("created_time", "")

        property_map = {
            "Title": {"title": [{"text": {"content": title}}]} if title else None,
            "URL": {"url": url, "type": "url"} if url else None,
            "Tags": {"type": "multi_select", "multi_select": [{"name": tag} for tag in tags]} if tags else None,
            "Created": {"date": {"start": created_time}, "type": "date"} if created_time else None,
        }

        properties_obj = {key: value for key, value in property_map.items() if value is not None}

        logger.debug(f"properties: {properties_obj}")
        return properties_obj

    @staticmethod
    def is_same_annotations_text(text_one: dict, text_another: dict):
        if text_one["type"] != "text" or text_another["type"] != "text":
            return False
        attributes = ["annotations", "href"]
        return all(text_one.get(attr) == text_another.get(attr) for attr in attributes)

    @staticmethod
    def merge_rich_text(rich_text: list):
        if not rich_text:
            return []
        merged_text = []
        current_text = rich_text[0]
        for text in rich_text[1:]:
            if Html2JsonBase.is_same_annotations_text(current_text, text):
                text_content = current_text["text"]["content"] + text["text"]["content"]
                current_text["plain_text"] = text_content
                current_text["text"]["content"] = text_content
            else:
                merged_text.append(current_text)
                current_text = text
        if current_text:
            merged_text.append(current_text)

        return merged_text

    @staticmethod
    def is_bold(tag_name: str, styles: dict) -> bool:
        if tag_name in ('b', 'strong'):
            return True

        font_weight = styles.get('font-weight', None)
        if font_weight is None:
            return False
        elif font_weight == 'bold':
            return True
        elif font_weight.isdigit() and int(font_weight) >= 700:
            return True
        return False

    @staticmethod
    def is_strikethrough(tag_name: str, styles: dict) -> bool:
        if tag_name in ('s', 'strike', 'del'):
            return True
        text_decoration = styles.get("text-decoration", "")
        return "line-through" in text_decoration

    @staticmethod
    def is_italic(tag_name: str, styles: dict) -> bool:
        if tag_name in ('i', 'em'):
            return True
        font_style = styles.get('font-style', "")
        return "italic" in font_style

    @staticmethod
    def is_underline(tag_name: str, styles: dict) -> bool:
        # A tuple of a single element requires a comma after the element
        if tag_name in ('u',):
            return True
        text_decoration = styles.get('text-decoration', "")
        return 'underline' in text_decoration

    @staticmethod
    def is_code(tag_name: str, styles: dict):
        if tag_name in ('code',):
            return True

        # Check if the font-family is monospace
        font_family = styles.get('font-family', "")
        monospace_fonts = {'courier', 'monospace'}
        if not font_family:
            return False
        for font in monospace_fonts:
            if font.lower() in font_family.lower():
                return True

    @staticmethod
    def _closest_color(r, g, b):
        closest_distance = float("inf")
        closest_color = None

        for color in Html2JsonBase._notion_color:
            distance = ((r - color.r) ** 2 + (g - color.g) ** 2 + (b - color.b) ** 2) ** 0.5
            if distance < closest_distance:
                closest_distance = distance
                closest_color = color.name

        return closest_color

    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def get_color(styles: dict, attrs):
        color = styles.get('color', "")
        if not color and 'color' in attrs:
            color = attrs['color']
        if not color:
            return "default"
        if color.startswith("rgb"):
            r, g, b = [int(x.strip()) for x in color[4:-1].split(",")]
        # Check if color is in hexadecimal format
        elif re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            r, g, b = Html2JsonBase._hex_to_rgb(color)
        else:
            return "default"

        return Html2JsonBase._closest_color(r, g, b)

    @classmethod
    def register(cls, input_type, subclass):
        cls._registry[input_type] = subclass

    @classmethod
    def create(cls, input_type, html_content):
        subclass = cls._registry.get(input_type)
        if subclass is None:
            raise ValueError(f"noknown: {input_type}")
        return subclass(html_content)
