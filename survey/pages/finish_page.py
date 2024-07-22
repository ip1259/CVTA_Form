from . import CustomPage


class FinishPage(CustomPage):
    def __init__(self):
        _BLOCK_DICTS: list[dict] = [{
            'block_type': "finish"
        }]
        super().__init__()
        self.load(_BLOCK_DICTS)
