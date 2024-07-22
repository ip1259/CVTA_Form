from .block import Block
import gradio as gr


class DescriptionBlock(Block):
    def __init__(self, title: str):
        self.title = title
        super().__init__()
        self._generate_body()

    def _generate_body(self):
        with gr.Row(variant="panel") as self.body:
            if self.title != "":
                gr.Markdown(f"*{self.title}*")
