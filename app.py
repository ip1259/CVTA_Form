import pandas as pd
import gradio as gr
from survey.pages.pages import *
from survey.pages.page import Page

survey = {'classname': "113F01_AIOT物聯網智慧應用設計班",
          'survey_desc': "本問卷用以了解學生對於師資滿意度進行調查，姓名僅有執行長及副執行長看的到，其餘老師會另外整理後以匿名方式提供老師日後教學上的參考，請放心填寫。",
          'teachers': ["林宜芳", "簡進士", "陳冠華", "陳柄宏", "王綉蘭", "林瓊嘉"]}

if __name__ == '__main__':
    head = HeadPage(survey.get('classname') + "教師滿意度調查問卷", survey.get('survey_desc'))
    body: list[Page] = [TeacherPage(teacher) for teacher in survey.get('teachers')]
    body.append(EmploymentPage())
    body.append(TAPage())
    pages = []
    with gr.Blocks() as app:
        head.page.render()
        for page in body:
            page.page.render()
            pages.append(page.page.blocks[list(page.page.blocks.keys())[0]])
    pages[-1].visible = False

    app.launch()
