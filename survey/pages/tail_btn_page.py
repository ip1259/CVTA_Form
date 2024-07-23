from .import CustomPage
from survey.blocks import TailButtonBlock
from gradio import Button


class TailButtonPage(CustomPage):
    def __init__(self, body_count: int):
        self._BLOCK_DICTS: list[dict] = [{
            'block_type': "tail_btn",
            'body_count': body_count
        }]
        super().__init__()
        self.page_blocks: list[TailButtonBlock] = []

    def get_buttons(self):
        _results = []
        for _b in self.page_blocks:
            if isinstance(_b, TailButtonBlock):
                for _interactive in _b.interactions:
                    if isinstance(_interactive, Button):
                        _results.append(_interactive)
        return _results

    def load_self(self):
        self.load(self._BLOCK_DICTS)
