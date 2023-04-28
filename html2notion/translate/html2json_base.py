import re
import os
from collections import namedtuple
from bs4 import NavigableString, Tag, PageElement
# from typing import Union
from enum import Enum
from ..utils import logger, config

class Block(Enum):
    FAIL = "fail"
    PARAGRAPH = "paragraph"
    QUOTE = "quote"
    NUMBERED_LIST = "numbered_list_item"
    BULLETED_LIST = "bulleted_list_item"
    HEADING = "heading"
    CODE = "code"
    DIVIDER = "divider"
    TABLE = "table"
    TO_DO = "to_do"

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
    def extract_text_and_parents(tag: PageElement, parents=[]):
        results = []
        if isinstance(tag, NavigableString):
            results.append((tag.text, parents))
            return results
        elif isinstance(tag, Tag):
            for child in tag.children:
                if isinstance(child, NavigableString):
                    if child.strip():
                        text = child.text
                        parent_tags = [p for p in parents + [tag]]
                        results.append((text, parent_tags))
                else:
                    results.extend(Html2JsonBase.extract_text_and_parents(child, parents + [tag]))
        return results

    @staticmethod
    def parse_one_style(tag_soup: Tag, text_params: dict):
        tag_name = tag_soup.name.lower()
        style = tag_soup.get('style', "")
        styles = {}
        if str and isinstance(style, str):
            styles = {rule.split(':')[0].strip(): rule.split(':')[1].strip() for rule in style.split(';') if rule}

        if Html2JsonBase.is_bold(tag_name, styles):
            text_params["bold"] = True
        if Html2JsonBase.is_italic(tag_name, styles):
            text_params["italic"] = True
        if Html2JsonBase.is_strikethrough(tag_name, styles):
            text_params["strikethrough"] = True
        if Html2JsonBase.is_underline(tag_name, styles):
            text_params["underline"] = True
        if Html2JsonBase.is_code(tag_name, styles):
            text_params["code"] = True

        color = Html2JsonBase.get_color(styles, tag_soup.attrs if tag_name else {})
        if color != 'default':
            text_params["color"] = color

        if tag_name == 'a':
            href = tag_soup.get('href', "")
            if not href:
                logger.warning("Link href is empty")
            text_params["url"] = href
        return

    # Process one tag and return a list of objects
    # <b><u>unlineline and bold</u></b>
    # <div><font color="#ff2600">Red color4</font></div>
    # <div> Code in super note</div>
    @staticmethod
    def generate_inline_obj(tag: PageElement):
        res_obj = []
        text_with_parents = Html2JsonBase.extract_text_and_parents(tag)
        for (text, parent_tags) in text_with_parents:
            text_params = {"plain_text": text}
            for parent in parent_tags:
                Html2JsonBase.parse_one_style(parent, text_params)

            if text_params.get("url", ""):
                text_obj = Html2JsonBase.generate_link(**text_params)
            else:
                text_obj = Html2JsonBase.generate_text(**text_params)
            if text_obj:
                res_obj.append(text_obj)
        return res_obj
    
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

        # style="-en-code: true"
        if styles.get('-en-code', "false") == "true":
            return True

        # Check if the font-family is monospace
        font_family = styles.get('font-family', "")
        monospace_fonts = {'courier', 'monospace'}
        if not font_family:
            return False
        for font in monospace_fonts:
            if font.lower() == font_family.lower():
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
        # If the color_values have 4 items, then it is RGBA and the last value is alpha
        # rgba(174, 174, 188, 0.2)
        if color.startswith("rgb"):
            color_values = [int(x.strip()) for x in re.findall(r'\d+', color)]
            if len(color_values) >= 3:
                r, g, b = color_values[:3]
                return Html2JsonBase._closest_color(r, g, b)
        # Check if color is in hexadecimal format
        elif re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            r, g, b = Html2JsonBase._hex_to_rgb(color)
            return Html2JsonBase._closest_color(r, g, b)

        return "default"

    def convert_paragraph(self, soup):
        json_obj = {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": []
            }
        }
        rich_text = json_obj["paragraph"]["rich_text"]
        text_obj = self.generate_inline_obj(soup)
        if text_obj:
            rich_text.extend(text_obj)
        return json_obj

    def convert_divider(self, soup):
        return {
            "object": "block",
            "type": "divider",
            "divider": {}
        }
    
    def convert_heading(self, soup):
        heading_map = {"h1": "heading_1", "h2": "heading_2", "h3": "heading_3",
                       "h4": "heading_3", "h5": "heading_3", "h6": "heading_3"}

        heading_level = heading_map.get(soup.name, "heading_3")
        json_obj = {
            "object": "block",
            "type": heading_level,
            heading_level: {
                "rich_text": []
            }
        }
        rich_text = json_obj[heading_level]["rich_text"]
        text_obj = self.generate_inline_obj(soup)
        if text_obj:
            rich_text.extend(text_obj)
        return json_obj

    # <ol><li><div>first</div></li><li><div>second</div></li><li><div>third</div></li></ol>
    def convert_numbered_list_item(self, soup):
        return self.convert_list_items(soup, 'numbered_list_item')

    # <ul><li><div>itemA</div></li><li><div>itemB</div></li><li><div>itemC</div></li></ul>
    def convert_bulleted_list_item(self, soup):
        return self.convert_list_items(soup, 'bulleted_list_item')

    def convert_list_items(self, soup, list_type):
        items = soup.find_all('li', recursive=True)
        if not items:
            logger.warning("No list items found in {soup}")

        json_arr = []
        for item in items:
            one_item = self._convert_one_list_item(item, list_type)
            if one_item:
                json_arr.append(one_item)
            else:
                logger.info(f'empty {item}')
        return json_arr

    def _convert_one_list_item(self, soup, list_type):
        if list_type not in {'numbered_list_item', 'bulleted_list_item'}:
            logger.warning(f'Not support list_type')

        json_obj = {
            "object": "block",
            list_type: {
                "rich_text": []
            },
            "type": list_type,
        }
        rich_text = json_obj[list_type]["rich_text"]
        text_obj = Html2JsonBase.generate_inline_obj(soup)
        if text_obj:
            rich_text.extend(text_obj)

        return json_obj

    # def convert_fail(self, soup):
    #     return {
    #         "object": "block",
    #         "type": "paragraph",
    #         "paragraph": {
    #             "rich_text": []
    #         }
    #     }

    @classmethod
    def register(cls, input_type, subclass):
        cls._registry[input_type] = subclass

    @classmethod
    def create(cls, input_type, html_content):
        subclass = cls._registry.get(input_type)
        if subclass is None:
            raise ValueError(f"noknown: {input_type}")
        return subclass(html_content)
