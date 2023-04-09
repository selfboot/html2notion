
class Html2JsonBase:
    _registry = {}

    def __init__(self, html_content):
        self.html_content = html_content
        self.children = []

    def process(self):
        raise NotImplementedError("Subclasses must implement this method")

    def get_res(self):
        return self.children
    
    @classmethod
    def register(cls, input_type, subclass):
        cls._registry[input_type] = subclass

    @classmethod
    def create(cls, input_type, html_content):
        subclass = cls._registry.get(input_type)
        if subclass is None:
            raise ValueError(f"noknown: {input_type}")
        return subclass(html_content)
