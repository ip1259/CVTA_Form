import gradio as gr
from survey.blocks.block import Block


class Page:
    def __init__(self):
        self.page_blocks: list[Block] = []
        self.page: gr.Blocks | None = None

    def _generate_page(self):
        with gr.Blocks() as _block:
            for pb in self.page_blocks:
                pb.body.render()

        self.page = _block
