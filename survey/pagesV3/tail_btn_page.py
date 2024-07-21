from .import CustomPage
from survey.blocksV3 import TailButtonBlock
from gradio import Button


class TailButtonPage(CustomPage):
    def __init__(self, body_count: int):
        _BLOCK_DICTS: list[dict] = [{
            'block_type': "tail_btn",
            'body_count': body_count
        }]
        super().__init__()
        self.page_blocks: list[TailButtonBlock] = []
        self.load(_BLOCK_DICTS)

    def get_buttons(self):
        _results = []
        for _b in self.page_blocks:
            if isinstance(_b, TailButtonBlock):
                for _interactive in _b.interactions:
                    if isinstance(_interactive, Button):
                        _results.append(_interactive)
        return _results
