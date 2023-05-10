# For notes that are clipped from web pages
# that are not written manually by Evernote and have rich text formatting,
# try to keep the format for conversion

from ..translate.html2json_base import Html2JsonBase

Default_Type = "default"


class Html2JsonDefault(Html2JsonBase):
    input_type = Default_Type

    def __init__(self, html_content, import_stat):
        super().__init__(html_content, import_stat)

    # todo
    def process(self):
        return Default_Type


Html2JsonBase.register(Default_Type, Html2JsonDefault)
