import json

from survey import exceptions as sError
import survey.pagesV2 as sPages
import gradio as gr

from gradio.themes.base import Base as grBase
import survey.themes.themes as sThemes
from survey.network import survey_client as client


class Survey:
    def __init__(self, parent_server):
        self.survey_id: str = ""
        self.survey_theme: tuple[grBase, str] | None = None
        self.heads: list = []
        self.bodies: list = []
        self.tail = None
        self.survey: gr.Blocks | None = None
        self.server = parent_server

    def get_rows_in_bodies(self):
        _results = []
        _results.extend([b.page for b in self.bodies])
        return _results

    def get_survey_input_components(self):
        _results = []
        for p in self.bodies:
            _results.extend(p.get_input_components())
        return _results

    def set_survey(self, file_path: str):
        """
        透過描述問卷的json檔案設定Survey物件
        Survey File Structure:
        {
        'survey_id': 字串-問卷的ID, 'survey_theme': "EMB"-預設值,
        'heads': [{
            'page_type': 'head',
            'title': "OOO班 教師滿意度調查",
            'desc': 字串-可選，描述性說明文字
            }],
        'bodies': [
            {'page_type': 'teacher', 'teacher': 字串-必須有-老師名稱, 'max_score': 整數-可選，最高分},
            {'page_type': 'ta', 'max_score': 整數-可選，最高分},
            {'page_type': 'employment'，就業輔導評分},
            {'page_type': "finish"，最後必需有，問卷送出後的顯示頁面},
            {
            'page_type': "custom"，自定義組合,
            'block_dicts':[
                {'block_type': "head", 'title': 字串，必須，標題, 'desc': 字串，必須，說明文字},頁首標題方塊
                {'block_type': "finish", 'title': 字串，可選，結束語},顯示結束的純文字方塊
                {
                'block_type': "score",-----評分問題
                'title': 字串，必須，描述問題,
                'must': 布林值，可選，設定問題是否為必填,
                'max_score': 整數值，可選，設定問題最高分,
                'max_score_desc': 字串，可選，設定最高分顯示標籤,
                'min_score_desc': 字串，可選，設定最低分顯示標籤},
                {
                'block_type': "suggestion",-----建議
                'title': 字串，必須，描述問題,
                'must': 布林值，可選，設定問題是否為必填
                }]
            }],
        'tail': {'page_type': 'tail_btn'必需，底部按鈕列}}
        :param file_path:描述問卷的json檔案位置
        :return: None
        """
        with open(file_path, 'r', encoding='utf8') as _sf:
            _survey_dict = json.load(_sf)
            self.load(_survey_dict)

    def on_survey_load(self, request: gr.Request):
        _ip = request.request.client.host
        self.server.clients[self, _ip] = client.SurveyClient(_ip, self)

    def on_survey_unload(self, request: gr.Request):
        _ip = request.request.client.host
        if (self, _ip) in self.server.clients.keys():
            print(self.server.clients[self, _ip])
            self.server.clients.pop(self, _ip)

    # with gr.Blocks(theme=self.survey_theme[0], css=self.survey_theme[1], js=sThemes.SurveyTheme.JS) as self.survey:
    #     for _hp in self.heads:
    #         self.survey.add(_hp.page)
    #         _hp.set_page_interactive()
    #     for _bp in self.bodies:
    #         self.survey.add(_bp.page)
    #         _bp.set_page_interactive()
    #     self.survey.add(self.tail.page)
    #     self.tail.set_page_interactive()

    def load(self, survey_dict: dict):
        if all(_i in survey_dict.keys() for _i in ['survey_id', 'survey_theme', 'heads', 'bodies', 'tail']):
            try:
                self.survey_id = survey_dict['survey_id']
                self.set_theme(survey_dict['survey_theme'])

                with gr.Blocks(theme=self.survey_theme[0], css=self.survey_theme[1],
                               js=sThemes.SurveyTheme.JS) as self.survey:
                    with gr.Column():
                        for _hp in survey_dict['heads']:
                            _t = self._parse_page(_hp)
                            self.heads.append(_t)
                            _t.set_page_interactive()
                        for _i, _bp in enumerate(survey_dict['bodies']):
                            _b = self._parse_page(_bp)
                            self.bodies.append(_b)
                            _b.set_page_interactive()
                            if len(self.bodies) == 1:
                                _b.page.visible = True
                            else:
                                _b.page.visible = False
                            if isinstance(_b, sPages.finish_page.FinishPage):
                                break
                            elif _i == len(survey_dict['bodies'])-1:
                                _b = sPages.finish_page.FinishPage(self.server, self)
                                self.bodies.append(_b)
                                _b.set_page_interactive()

                        self.tail = self._parse_page(survey_dict['tail'])
                        self.tail.set_page_interactive()
                        self.survey.load(self.on_survey_load)
                        self.survey.unload(self.on_survey_unload)

            except Exception as e:
                print(e)
                raise sError.UnableLoadSurvey(-1)
        else:
            raise sError.UnableLoadSurvey(0)

    def _parse_page(self, page_dict: dict):
        if "page_type" in page_dict.keys():
            try:
                match page_dict['page_type']:
                    case "tail_btn":
                        return sPages.tail_btn_page.TailButtonPage(self.server, self)
                    case "head":
                        _hp = sPages.head_page.HeadPage(page_dict['title'], self.server, self)
                        if "desc" in page_dict.keys():
                            if not isinstance(page_dict['desc'], str):
                                raise sError.UnableParsePage(3, f"{page_dict['page_type']}-'desc'")
                            _hp.set_desc(page_dict['desc'])
                        return _hp
                    case "finish":
                        _fp = sPages.finish_page.FinishPage(self.server, self)
                        return _fp
                    case "teacher":
                        _tp = sPages.teacher_page.TeacherPage(page_dict['teacher'], self.server, self)
                        if "max_score" in page_dict.keys():
                            if not isinstance(page_dict['max_score'], int):
                                raise sError.UnableParsePage(3, f"{page_dict['page_type']}-'max_score'")
                            _tp.set_max_score(page_dict['max_score'])
                        return _tp
                    case "ta":
                        _tp = sPages.ta_page.TAPage(self.server, self)
                        if "max_score" in page_dict.keys():
                            if not isinstance(page_dict['max_score'], int):
                                raise sError.UnableParsePage(3, f"{page_dict['page_type']}-'max_score'")
                            _tp.set_max_score(page_dict['max_score'])
                        return _tp
                    case "employment":
                        _ep = sPages.employment_page.EmploymentPage(self.server, self)
                        return _ep
                    case "custom":
                        _cp = sPages.custom_page.CustomPage(self.server, self)
                        _cp.load(page_dict['block_dicts'])
                        return _cp
                    case _:
                        raise sError.UnableParsePage(1)
            except Exception as e:
                print(e)
                raise sError.UnableParsePage(2)
        else:
            raise sError.UnableParsePage(0)

    def set_theme(self, theme: str):
        match theme:
            case "EMB":
                self.survey_theme = sThemes.SurveyTheme.EMB
            case _:
                self.survey_theme = sThemes.SurveyTheme.EMB
