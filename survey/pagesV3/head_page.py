from . import CustomPage


class HeadPage(CustomPage):
    DEFAULT_DESC = "本問卷用以了解學生對於師資滿意度進行調查，以匿名方式提供老師日後教學上的參考，請放心填寫。\n*代表必填"

    def __init__(self, title: str,
                 desc: str = DEFAULT_DESC):
        self._title = title
        self._desc = desc
        self._BLOCK_DICTS: list[dict] = [{
            'block_type': "head", 'title': self._title, 'desc': self._desc
        }]
        super().__init__()
        self.load(self._BLOCK_DICTS)

    def set_desc(self, desc: str):
        self._desc = desc
        self.load(self._BLOCK_DICTS)

    def set_title(self, title: str):
        self._title = title
        self.load(self._BLOCK_DICTS)
