from survey.pages.page import Page
from survey.blocks.score_block import ScoreBlock
from survey.blocks.suggestion_block import SuggestionBlock


class TAPage(Page):
    Q1 = "1.請問助教的課業諮詢服務(協助上課、回覆/解決問題)滿意程度?"
    Q2 = "2.請問助教的專業程度是否滿意?"
    Q3 = "3.對助教的建議或想說的話? (最少10個字或更多)非必填"

    def __init__(self):
        super().__init__()
        self.page_blocks.append(ScoreBlock(TAPage.Q1))
        self.page_blocks.append(ScoreBlock(TAPage.Q2))
        self.page_blocks.append(SuggestionBlock(TAPage.Q3))
        super()._generate_page()


if __name__ == '__main__':
    ta = TAPage()
    ta.page.launch()
