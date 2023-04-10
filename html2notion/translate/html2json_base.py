from cssutils.css import Property
from ..utils import logger


class Html2JsonBase:
    _registry = {}
    text_annotations = {
        "bold": bool,
        "italic": bool,
        "strikethrough": bool,
        "underline": bool,
        "code": bool,
        "color": str,
    }

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
            if key == "plain_text" or key not in Html2JsonBase.text_annotations:
                continue
            if not isinstance(value, Html2JsonBase.text_annotations[key]):
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

    @classmethod
    def register(cls, input_type, subclass):
        cls._registry[input_type] = subclass

    @classmethod
    def create(cls, input_type, html_content):
        subclass = cls._registry.get(input_type)
        if subclass is None:
            raise ValueError(f"noknown: {input_type}")
        return subclass(html_content)
