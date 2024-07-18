from survey.blocks.score_block import ScoreBlock
from survey.pages.page import Page
import gradio as gr


class EmploymentPage(Page):
    Q1 = "1.請問就業輔導活動『廠商』安排是否符合課程所學之專業相關?*"
    Q2 = "2.請問就業輔導活動『時間』安排(課程期程)您滿意程度?*"
    Q3 = "3.請問就業輔導老師『態度』(回覆問題、了解廠商)您滿意程度?*"
    Q4 = "4.請問就業輔導活動前對於『廠商資訊』(公司地址、職缺資訊等)是否有足夠資訊?*"

    def __init__(self):
        super().__init__()
        self._generate_page()

    def _generate_page(self):
        with gr.Row() as _row:
            with gr.Column():
                self.page_blocks.append(
                    ScoreBlock(EmploymentPage.Q1, min_score_desc="非常不符合", max_score_desc="非常符合"))
                self.page_blocks.append(ScoreBlock(EmploymentPage.Q2))
                self.page_blocks.append(ScoreBlock(EmploymentPage.Q3))
                self.page_blocks.append(ScoreBlock(EmploymentPage.Q4, min_score_desc="非常不足", max_score_desc="非常充足"))
        self.page = _row


if __name__ == '__main__':
    with gr.Blocks() as demo:
        em = EmploymentPage()
    demo.launch()
