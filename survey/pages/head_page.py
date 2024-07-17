from survey.blocks.head_block import HeadBlock
from survey.pages.page import Page


class HeadPage(Page):
    def __init__(self, title: str, desc: str):
        super().__init__()
        self.page_blocks.append(HeadBlock(title, desc))
        super()._generate_page()


if __name__ == '__main__':
    head = HeadPage("113F06", "描述2")
    head.page.launch()
