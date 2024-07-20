import gradio as gr
from survey.blocksV2.block import Block
from survey.surveys import survey


class HeadBlock(Block):
    def __init__(self, title: str, desc: str, parent_survey: survey.Survey):
        self._desc = desc
        super().__init__(title, parent_survey)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(min_width=0, scale=1):
                pass
            with gr.Column(variant="panel", scale=3, min_width=640):
                gr.Markdown(f'# <div align="center">{self.title}</div>')
                gr.Markdown(self._desc)
            with gr.Column(min_width=0, scale=1):
                pass
