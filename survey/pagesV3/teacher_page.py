from . import CustomPage


class TeacherPage(CustomPage):
    Q1 = "1.請問{0}老師的上課態度(上課認真、回覆問題、課程準備)您滿意程度?*"
    Q2 = "2.請問{0}老師的上課技巧(表達能力、教學方式、電腦操作、互動方式)滿意程度?*"
    Q3 = "3.請問{0}老師提供的上課教材充足?*"
    Q4 = "4.請問{0}老師的上下課時間拿捏是否適當?*"
    Q5 = "5.對{0}老師的建議或想說的話?  (非必填)"

    def __init__(self, _teacher: str, max_score: int = 5):
        self._teacher = _teacher
        self._max_score = max_score
        self._BLOCK_DICTS: list[dict] = [{
            'block_type': "score", 'title': TeacherPage.Q1.format(self._teacher), 'max_score': self._max_score
        }, {
            'block_type': "score", 'title': TeacherPage.Q2.format(self._teacher), 'max_score': self._max_score
        }, {
            'block_type': "score", 'title': TeacherPage.Q3.format(self._teacher), 'max_score': self._max_score
        }, {
            'block_type': "score", 'title': TeacherPage.Q4.format(self._teacher), 'max_score': self._max_score
        }, {
            'block_type': "suggestion", 'title': TeacherPage.Q5.format(self._teacher)
        }]
        super().__init__()
        self.load(self._BLOCK_DICTS)

    def set_teacher(self, teacher: str):
        self._teacher = teacher
        self.load(self._BLOCK_DICTS)

    def set_max_score(self, max_score: int):
        self._max_score = max_score
        self.load(self._BLOCK_DICTS)
