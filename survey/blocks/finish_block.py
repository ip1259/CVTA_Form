from .block import Block
import gradio as gr


class FinishBlock(Block):
    def __init__(self, title: str = "我們已收到您的回覆，感謝您的耐心填寫"):
        super().__init__(title)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as _fin:
            with gr.Column(min_width=0, scale=1):
                pass
            with gr.Column(variant="panel", scale=3, min_width=640):
                gr.Markdown(f"## {self.title}")
            with gr.Column(min_width=0, scale=1):
                pass
        self.body = _fin
