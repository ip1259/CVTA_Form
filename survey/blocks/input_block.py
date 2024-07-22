import gradio as gr

from .interactive_block import InteractiveBlock


class InputBlock(InteractiveBlock):

    def __init__(self, title: str, desc: str, must: bool):
        self.must = must
        self.title = title
        self.desc = desc
        super().__init__()

    def get_input_components(self) -> tuple[bool, gr.components.Component, str]:
        return self.must, self.interactions[0], self.title

    def set_interactive_triggered(self, user_store: gr.State):
        pass
