import gradio as gr

from survey.blocks.finish_block import FinishBlock
from survey.pages.page import Page


class FinishPage(Page):
    def __init__(self, parent):
        super().__init__(parent)
        self._generate_page()

    def _generate_page(self):
        with gr.Row() as _row:
            with gr.Column():
                self.page_blocks.append(FinishBlock())
        self.page = _row
