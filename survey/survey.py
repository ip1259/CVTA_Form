import os.path

import gradio.components.base
from gradio.themes.base import Base

import survey.blocks.input_block
from survey.pages.page import Page
from survey.pages.pages import *
from survey.themes.themes import *

import openpyxl


class Survey:
    def __init__(self, class_name: str, teachers: list[str],
                 survey_id: str,
                 has_ta: bool,
                 survey_desc: str = "本問卷用以了解學生對於師資滿意度進行調查，以匿名方式提供老師日後教學上的參考，請放心填寫。\n*代表必填",
                 survey_theme: Base = SurveyTheme.EMB):
        self.has_ta = has_ta
        self.survey_id = survey_id
        self.survey_theme = survey_theme
        self.survey_desc = survey_desc
        self.teachers = teachers
        self.class_name = class_name
        self.head: Page | None = None
        self.body: list[Page] | None = []
        self.cur_body_index: int = -1
        self.clients: dict[str, SurveyClient] = {}
        self.response: dict[str, SurveyResponse] | None = {}

    def start_survey(self):
        def set_cur_body(index: int, _br: list[gradio.components.base.Component]):
            self.cur_body_index = index
            self.cur_body_index = min(self.cur_body_index, len(_br) - 1)
            self.cur_body_index = max(self.cur_body_index, 0)
            for _i, _r in enumerate(_br):
                if isinstance(_r, gr.Row):
                    if _i == self.cur_body_index:
                        _r.visible = True
                    else:
                        _r.visible = False

        with gr.Blocks(js=SurveyTheme.JS, css=SurveyTheme.EMB_CSS, theme=self.survey_theme) as survey:
            _body_rows: list[gradio.components.base.Component] = []
            self.head = HeadPage(self.class_name + "教師滿意度調查問卷", self.survey_desc, self)
            for i, teacher in enumerate(self.teachers):
                with gr.Row(visible=False) as r:
                    _t = TeacherPage(teacher, self)
                    self.body.append(_t)
                _body_rows.append(r)
            with gr.Row(visible=False) as emp_row:
                _e = EmploymentPage(self)
                self.body.append(_e)
                _body_rows.append(emp_row)
            if self.has_ta:
                with gr.Row(visible=False) as ta_row:
                    _ta = TAPage(self)
                    self.body.append(_ta)
                    _body_rows.append(ta_row)

            set_cur_body(0, _body_rows)

            with gr.Row():
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="default", scale=3, min_width=640):
                    with gr.Row():
                        with gr.Row(visible=self.cur_body_index > 0) as prev_warp:
                            prev_button = gr.Button("返回", min_width=75, scale=1)
                        with gr.Column(scale=10, min_width=0):
                            pass
                        with gr.Row(visible=(self.cur_body_index < len(_body_rows) - 1)) as next_warp:
                            next_button = gr.Button("繼續", min_width=75, scale=1)
                        with gr.Row(visible=(self.cur_body_index == len(_body_rows) - 1)) as send_warp:
                            send_button = gr.Button("送出", min_width=75, scale=1, elem_id="sendButton")

                with gr.Column(min_width=0, scale=1):
                    pass

            def next_body(request: gr.Request):
                if request:
                    if self.body[self.cur_body_index].must_has_done(request.request.client.host):
                        set_cur_body(self.cur_body_index + 1, _body_rows)
                _result = []
                for _r in _body_rows:
                    if isinstance(_r, gr.Row):
                        _result.append(_r.update(_r.visible))
                _result.extend([prev_warp.update(self.cur_body_index > 0),
                                next_warp.update((self.cur_body_index < len(
                                    _body_rows) - 1)),
                                send_warp.update((self.cur_body_index == len(
                                    _body_rows) - 1))])
                return _result

            def prev_body():
                set_cur_body(self.cur_body_index - 1, _body_rows)
                _result = []
                for _r in _body_rows:
                    if isinstance(_r, gr.Row):
                        _result.append(_r.update(_r.visible))
                _result.extend([prev_warp.update(self.cur_body_index > 0),
                                next_warp.update((self.cur_body_index < len(
                                    _body_rows) - 1)),
                                send_warp.update((self.cur_body_index == len(
                                    _body_rows) - 1))
                                ])
                return _result

            def send_click(request: gr.Request):
                if request:
                    _ip = request.request.client.host
                    print(self.clients[_ip].response)
                    self.clients[_ip].save_response()

            btn_outputs = [_r for _r in _body_rows]
            btn_outputs.extend([prev_warp, next_warp, send_warp])
            to_top_js = """
                        function to_top() {
                            window.scrollTo(0,0);
                        }
                        """
            next_button.click(next_body, None,
                              outputs=btn_outputs, js=to_top_js)
            prev_button.click(prev_body, None,
                              outputs=btn_outputs, js=to_top_js)
            send_button.click(send_click)

            def survey_load(request: gr.Request):
                _ip = request.request.client.host
                self.clients[_ip] = SurveyClient(_ip, self)

            def survey_unload(request: gr.Request):
                _ip = request.request.client.host
                self.clients.pop(_ip)

            survey.load(survey_load)
            survey.unload(survey_unload)
        return survey

    def get_survey_input_components(self):
        _results = []
        for p in self.body:
            _results.extend(p.get_input_components())
        return _results


class SurveyResponse:
    def __init__(self, parent: Survey):
        self.parent = parent
        # example self.response[an InputBlock Object as KEY] = (Question, Must Answer Or Not, Value)
        self.response: dict[survey.blocks.input_block.InputBlock, tuple[str, bool, str | int | float]] = {}
        self.init_response()

    def init_response(self):
        _inputs = self.parent.get_survey_input_components()
        for i in _inputs:
            self.set_response(i, None)

    def set_response(self, input_block: survey.blocks.input_block.InputBlock, value):
        self.response[input_block] = (input_block.title, input_block.must, value)


class SurveyClient:
    def __init__(self, ip: str, parent: Survey):
        self.ip = ip
        self.parent = parent
        self.response = SurveyResponse(parent)
        self.cur_body_index: int = -1

    def save_response(self):
        _path = os.getcwd()
        _path = os.path.join(_path, "responses")
        if not os.path.exists(_path):
            os.mkdir(_path)
        _wb = None
        _path = os.path.join(_path, self.parent.survey_id + ".xlsx")
        if not os.path.exists(_path):
            _wb = openpyxl.Workbook()
            _wb.create_sheet("表單回覆")
            _wb.remove_sheet(_wb["Sheet"])
            _ws = _wb["表單回覆"]
            _titles = ["IP"]
            _titles.extend([_t[0] for _t in self.response.response.values()])
            _ws.append(_titles)
            _wb.save(_path)
        _wb = openpyxl.load_workbook(_path)
        _response = [self.ip]
        _response.extend([_t[2] for _t in self.response.response.values()])
        for r in _response:
            if r is None:
                r = ""
        _ws = _wb["表單回覆"]
        _ws.append(_response)
        _wb.save(_path)
