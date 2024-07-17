from survey.pages.page import Page
from survey.blocks.score_block import ScoreBlock
from survey.blocks.suggestion_block import SuggestionBlock


class TeacherPage(Page):
    Q1 = "1.請問{0}老師的上課態度(上課認真、回覆問題、課程準備)您滿意程度?"
    Q2 = "2.請問{0}老師的上課技巧(表達能力、教學方式、電腦操作、互動方式)滿意程度?"
    Q3 = "3.請問{0}老師提供的上課教材充足?"
    Q4 = "4.請問{0}老師的上下課時間拿捏是否適當?"
    Q5 = "5.對{0}老師的建議或想說的話?  (非必填)"

    def __init__(self, _teacher: str, max_score: int = 5):
        super().__init__()
        self.page_blocks.append(ScoreBlock(TeacherPage.Q1.format(_teacher), max_score))
        self.page_blocks.append(ScoreBlock(TeacherPage.Q2.format(_teacher), max_score))
        self.page_blocks.append(ScoreBlock(TeacherPage.Q3.format(_teacher), max_score))
        self.page_blocks.append(ScoreBlock(TeacherPage.Q4.format(_teacher), max_score))
        self.page_blocks.append(SuggestionBlock(TeacherPage.Q5.format(_teacher)))
        super()._generate_page()


if __name__ == '__main__':
    teacher = TeacherPage("簡進士")
    teacher.page.launch()
