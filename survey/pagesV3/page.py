import gradio as gr

from survey.blocksV3 import *


class Page:
    def __init__(self):
        self.page_blocks: list[Block] = []
        self.page: gr.Row | None = None

    def _generate_page(self):
        pass

    def get_input_components(self) -> list[tuple[bool, gr.components.Component]]:
        _result = []
        for b in self.page_blocks:
            if isinstance(b, input_block.InputBlock):
                _result.append(b.get_input_components())
        return _result
