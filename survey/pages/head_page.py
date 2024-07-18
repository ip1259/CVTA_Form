import gradio as gr

from survey.blocks.head_block import HeadBlock
from survey.pages.page import Page


class HeadPage(Page):
    def __init__(self, title: str, desc: str):
        super().__init__()
        self._title = title
        self._desc = desc
        self._generate_page()

    def _generate_page(self):
        with gr.Row() as _row:
            with gr.Column():
                self.page_blocks.append(HeadBlock(self._title, self._desc))
        self.page = _row


if __name__ == '__main__':

    with gr.Blocks() as demo:
        head = HeadPage("113F06", "描述2")
    demo.launch()
