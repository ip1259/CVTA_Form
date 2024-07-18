import gradio as gr


class Block:
    def __init__(self, title: str):
        self.body: gr.Column | None = None
        self._title = title
        self._generate_body()

    def _generate_body(self):
        pass
