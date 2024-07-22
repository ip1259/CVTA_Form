from .block import Block
import gradio as gr


class FinishBlock(Block):
    def __init__(self, title: str = "我們已收到您的回覆，感謝您的耐心填寫"):
        self.title = title
        super().__init__()
        self._generate_body()

    def _generate_body(self):
        with gr.Row(variant="panel") as self.body:
            gr.Markdown(f"## {self.title}")
