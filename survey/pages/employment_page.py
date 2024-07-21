from survey.pages import custom_page


class EmploymentPage(custom_page.CustomPage):
    Q1 = "1.請問就業輔導活動『廠商』安排是否符合課程所學之專業相關?*"
    Q2 = "2.請問就業輔導活動『時間』安排(課程期程)您滿意程度?*"
    Q3 = "3.請問就業輔導老師『態度』(回覆問題、了解廠商)您滿意程度?*"
    Q4 = "4.請問就業輔導活動前對於『廠商資訊』(公司地址、職缺資訊等)是否有足夠資訊?*"

    def __init__(self, parent_server, parent_survey):
        _BLOCK_DICTS: list[dict] = [{
            'block_type': "score", 'title': EmploymentPage.Q1.format(),
            'max_score_desc': "非常符合", 'min_score_desc': "非常不符合"
        }, {
            'block_type': "score", 'title': EmploymentPage.Q2.format()
        }, {
            'block_type': "score", 'title': EmploymentPage.Q3.format()
        }, {
            'block_type': "score", 'title': EmploymentPage.Q4.format(),
            'max_score_desc': "非常充足", 'min_score_desc': "非常不足"
        }]
        super().__init__(parent_server, parent_survey)
        self.load(_BLOCK_DICTS)


if __name__ == '__main__':
    import gradio as gr

    with gr.Blocks() as demo:
        tp = EmploymentPage(None, None)
    demo.launch()
