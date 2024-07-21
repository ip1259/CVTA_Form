from . import CustomPage


class TAPage(CustomPage):
    Q1 = "1.請問助教的課業諮詢服務(協助上課、回覆/解決問題)滿意程度?*"
    Q2 = "2.請問助教的專業程度是否滿意?*"
    Q3 = "3.對助教的建議或想說的話? 非必填"

    def __init__(self, max_score: int = 5):
        self._max_score = max_score
        self._BLOCK_DICTS: list[dict] = [{
            'block_type': "score", 'title': TAPage.Q1.format(), 'max_score': self._max_score
        }, {
            'block_type': "score", 'title': TAPage.Q2.format(), 'max_score': self._max_score
        }, {
            'block_type': "suggestion", 'title': TAPage.Q3.format()
        }]
        super().__init__()
        self.load(self._BLOCK_DICTS)

    def set_max_score(self, max_score: int):
        self._max_score = max_score
        self.load(self._BLOCK_DICTS)