import gradio as gr

from .interactive_block import InteractiveBlock


class InputBlock(InteractiveBlock):

    def __init__(self, title: str, must: bool):
        self.must = must
        self.title = title
        super().__init__()

    def get_input_components(self) -> tuple[bool, gr.components.Component]:
        return self.must, self.interactions[0]

    def set_interactive_triggered(self, user_store: gr.State):
        pass
