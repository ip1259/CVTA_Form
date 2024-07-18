import gradio as gr

from survey.blocks.block import Block
from survey.blocks.input_block import InputBlock


class Page:
    def __init__(self, parent):
        self.parent = parent
        self.page_blocks: list[Block] = []
        self.page: gr.Row | None = None

    def _generate_page(self):
        pass

    def get_page_result(self, ip: str):
        _results = []
        _cursor = 0
        for i, b in enumerate(self.page_blocks):
            if isinstance(b, InputBlock):
                _results.append((type(b), b.must, b.get_result(ip)))
                _cursor += 1
        return _results

    def must_has_done(self, ip: str):
        _results = self.get_page_result(ip)
        if len(_results) != 0:
            for r in _results:
                if r[1] and (r[2] is None):
                    return False
        return True

    def get_input_components(self):
        _result = []
        for b in self.page_blocks:
            if isinstance(b, InputBlock):
                _result.append(b)
        # print(_result)
        return _result

    def get_page_response(self, ip: str):
        _response = []
        for b in self.page_blocks:
            if isinstance(b, InputBlock):
                _response.append(b.get_response(ip))
        return _response
