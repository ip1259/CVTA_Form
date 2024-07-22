from .block import Block
import gradio as gr


class InteractiveBlock(Block):
    def __init__(self):
        self.interactions: list[gr.components.Component] = []
        super().__init__()

    def set_interactive_triggered(self, user_store: gr.State):
        pass
