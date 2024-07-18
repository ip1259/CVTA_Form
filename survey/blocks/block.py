import gradio as gr


class Block:
    def __init__(self, title: str):
        self.body: gr.Column | None = None
        self.title = title

    def _generate_body(self):
        pass
