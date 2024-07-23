from . import CustomPage


class FinishPage(CustomPage):
    def __init__(self):
        self._BLOCK_DICTS: list[dict] = [{
            'block_type': "finish"
        }]
        super().__init__()

    def load_self(self):
        self.load(self._BLOCK_DICTS)
