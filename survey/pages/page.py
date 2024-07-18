import gradio as gr
import gradio.blocks

from survey.blocks.block import Block
from survey.blocks.input_block import InputBlock


class Page:
    def __init__(self):
        self.page_blocks: list[Block] = []
        self.page: gr.Row | None = None

    def _generate_page(self):
        pass

    def get_page_result(self, *args):
        _results = []
        _cursor = 0
        for i, b in enumerate(self.page_blocks):
            if isinstance(b, InputBlock):
                _results.append((type(b), b.must, args[_cursor]))
                _cursor += 1
        return _results

    def must_has_done(self):
        _results = self.get_page_result()
        if len(_results) != 0:
            for r in _results:
                if r[1] and (r[2] is None):
                    return False
        return True

    def get_input_components(self):
        _result = []
        for b in self.page_blocks:
            if isinstance(b, InputBlock):
                _result.extend(b.get_input_components())
        # print(_result)
        return _result
