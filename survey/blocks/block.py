import gradio as gr


class Block:
    def __init__(self, title: str, parent_survey):
        self.body: gr.Row | None = None
        self.title = title
        self.parent_survey = parent_survey

    def _generate_body(self):
        pass
