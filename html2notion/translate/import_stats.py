from pathlib import Path
from enum import Enum


class StatLevel(Enum):
    EXCEPTION = "exception"
    LOSS = "loss"
    SUCC = "success"


class ImportStats:
    def __init__(self):
        self.text_count = 0
        self.image_count = 0
        self.notion_text_count = 0
        self.notion_image_count = 0
        self.skip_tag = []
        self.exception = None
        self.filename = "None"
        self.html_content = ""
        self.notion_content = ""

    def add_text(self, text: str):
        self.text_count += len(text)
        self.html_content += text

    def add_notion_text(self, text: str):
        self.notion_content += text
        self.notion_text_count += len(text)

    def add_image(self, count: int):
        self.image_count += count

    def add_notion_image(self, count: int):
        self.notion_image_count += count

    def add_skip_tag(self, tag):
        self.skip_tag.append(tag)

    def set_filename(self, filename: Path):
        self.filename = filename

    def set_exception(self, exception: Exception):
        self.exception = exception

    def get_level(self):
        if self.exception:
            return StatLevel.EXCEPTION.value
        if self.notion_text_count < self.text_count:
            return StatLevel.LOSS.value
        return StatLevel.SUCC.value

    def __str__(self):
        if self.get_level() == StatLevel.EXCEPTION.value:
            return f"[red]{str(self.exception)}[/red]"
        msg = ""
        if self.get_level() == StatLevel.LOSS.value:
            if self.text_count != self.notion_text_count:
                msg += f"Text Len {self.text_count} -> {self.notion_text_count}, Loss [yellow]{self.text_count-self.notion_text_count}[/yellow]"

            msg += '\nDetail: [yellow]' + ";".join([repr(s) for s in self.skip_tag])[:500] + "[/yellow]"
        return msg

    def get_detail(self):
        return f"filename: {self.filename}, {self.text_count} text, {self.image_count} image\nNotion {self.notion_text_count} text, {self.notion_image_count} image\n{self.skip_tag}"


if __name__ == '__main__':
    task_stats = ImportStats()
    task_stats.add_text(100)
    task_stats.add_image(20)
    task_stats.add_notion_text(80)
    task_stats.add_notion_image(15)
    task_stats.set_exception(Exception("Some error occurred"))

    print(task_stats)
