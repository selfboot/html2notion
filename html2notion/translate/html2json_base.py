from collections import namedtuple
from cssutils.css import Property
from ..utils import logger


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

    notion_block_types = {
        "paragraph": "paragraph",
        "quote": "quote",
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

    def __init__(self, html_content):
        self.html_content = html_content
        self.children = []

    def process(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_res(self):
        return self.children

    @staticmethod
    def generate_text(**kwargs):
        if not kwargs.get("plain_text", ""):
            return
        text_obj = {}
        text_obj["plain_text"] = kwargs.get("plain_text", "")
        text_obj["type"] = "text"
        text_obj["text"] = {}
        text_obj["text"]["content"] = kwargs.get("plain_text", "")
        text_obj["annotations"] = {}
        for key, value in kwargs.items():
            if key == "plain_text" or key not in Html2JsonBase._text_annotations:
                continue
            if not isinstance(value, Html2JsonBase._text_annotations[key]):
                logger.warn(f"Invalid annotation: {key}={value}")
            text_obj["annotations"][key] = value
        if not text_obj["annotations"]:
            del text_obj["annotations"]
        return text_obj

    @staticmethod
    def is_bold(tag_name: str, styles: Property) -> bool:
        if tag_name in ('b', 'strong'):
            return True

        font_weight = styles.getPropertyValue('font-weight', None)
        if font_weight is None:
            return False
        elif font_weight == 'bold':
            return True
        elif font_weight.isdigit() and int(font_weight) >= 700:
            return True
        return False

    @staticmethod
    def is_strikethrough(tag_name: str, styles: Property) -> bool:
        if tag_name in ('s', 'strike', 'del'):
            return True
        text_decoration = styles.getPropertyValue("text-decoration", None)
        return "line-through" in text_decoration

    @staticmethod
    def is_italic(tag_name: str, styles: Property) -> bool:
        if tag_name in ('i', 'em'):
            return True
        font_style = styles.getPropertyValue('font-style', None)
        return "italic" in font_style

    @staticmethod
    def is_underline(tag_name: str, styles: Property) -> bool:
        # A tuple of a single element requires a comma after the element
        if tag_name in ('u',):
            return True
        text_decoration = styles.getPropertyValue('text-decoration', None)
        return 'underline' in text_decoration

    @staticmethod
    def is_code(tag_name: str, styles: Property):
        if tag_name in ('code',):
            return True

        # Check if the font-family is monospace
        font_family = styles.getPropertyValue('font-family', None)
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
    def get_color(styles: Property):
        color = styles.getPropertyValue('color', None)
        if not color:
            return "default"
        if color.startswith("rgb"):
            r, g, b = [int(x.strip()) for x in color[4:-1].split(",")]
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
