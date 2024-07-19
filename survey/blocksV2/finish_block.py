from .block import Block
from survey.surveys import survey
import gradio as gr


class FinishBlock(Block):
    def __init__(self, parent_survey: survey.Survey, title: str = "我們已收到您的回覆，感謝您的耐心填寫"):
        super().__init__(title, parent_survey)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(min_width=0, scale=1):
                pass
            with gr.Column(variant="panel", scale=3, min_width=640):
                gr.Markdown(f"## {self.title}")
            with gr.Column(min_width=0, scale=1):
                pass
