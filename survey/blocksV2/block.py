import gradio as gr
from survey.surveys import survey


class Block:
    def __init__(self, title: str, parent_survey: survey.Survey):
        self.body: gr.Row | None = None
        self.title = title
        self.parent_survey = parent_survey

    def _generate_body(self):
        pass
