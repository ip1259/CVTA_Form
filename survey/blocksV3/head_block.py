import gradio as gr
from .block import Block


class HeadBlock(Block):
    def __init__(self, title: str, desc: str):
        self.title = title
        self._desc = desc
        super().__init__()
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(variant="panel", min_width=640):
                gr.Markdown(f'# <div align="center">{self.title}</div>')
                gr.Markdown(self._desc)
