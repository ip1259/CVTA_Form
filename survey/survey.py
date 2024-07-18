import gradio as gr
from survey.pages.pages import *
from survey.pages.page import Page
from survey.themes.themes import *
from gradio.themes.base import Base


class Survey:
    def __init__(self, class_name: str, teachers: list[str],
                 survey_desc: str = "本問卷用以了解學生對於師資滿意度進行調查，以匿名方式提供老師日後教學上的參考，請放心填寫。",
                 survey_theme: Base = SurveyTheme.EMB):
        self.survey_theme = survey_theme
        self.survey_desc = survey_desc
        self.teachers = teachers
        self.class_name = class_name
        self.head: Page | None = None
        self.body: list[Page] | None = []
        self.cur_body: int = -1

    def start_survey(self):
        with gr.Blocks(js=SurveyTheme.JS, theme=self.survey_theme) as survey:
            _body_rows = {}
            self.head = HeadPage(self.class_name + "教師滿意度調查問卷", self.survey_desc)
            # with gr.Row(visible=True) as r1:
            #     TeacherPage(self.teachers[0])
            # with gr.Row(visible=False) as r2:
            #     TeacherPage(self.teachers[2])
            for i, teacher in enumerate(self.teachers):
                with gr.Row() as r:
                    TeacherPage(teacher)
                _body_rows[i] = r
                _body_rows[i].visible = False
            self.cur_body = 0
            _body_rows[self.cur_body].visible = True

            with gr.Row():
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="default", scale=3, min_width=640):
                    with gr.Row():
                        prev_button = gr.Button("返回", min_width=75, scale=1)
                        with gr.Column(scale=10, min_width=0):
                            pass
                        next_button = gr.Button("繼續", min_width=75, scale=1)

                with gr.Column(min_width=0, scale=1):
                    pass

            def next_body():
                print(self.cur_body)
                self.cur_body += 1
                self.cur_body = min(self.cur_body, len(_body_rows) - 1)
                return [_body_rows[self.cur_body-1].update(False), _body_rows[self.cur_body].update(True)]
                # print(r1, r2)
                # return r1.update(False), r2.update(True)

            next_button.click(next_body, None, [_body_rows[int(max(0, self.cur_body-1))], _body_rows[self.cur_body]])
            # next_button.click(next_body, None, [r1, r2])

        return survey
