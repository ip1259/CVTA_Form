from __future__ import annotations
from typing import TYPE_CHECKING
import gradio as gr
import survey.exceptions as sError

if TYPE_CHECKING:
    from gradio.themes.base import Base as grBase
    import survey.pagesV2 as sPages
    import survey.themes.themes as sThemes
    from survey.network import survey_server as server


class Survey:
    def __init__(self, parent_server: server.SurveyServer):
        self.survey_id: str = ""
        self.survey_theme: tuple[grBase, str] | None = None
        self.heads: list[sPages.page.Page] = []
        self.bodies: list[sPages.page.Page] = []
        self.tail: sPages.page.Page | None = None
        self.survey: gr.Blocks | None = None
        self.server: server.SurveyServer = parent_server

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

        :param file_path:
        :return: None
        """
        pass

    def generate_survey(self):
        with gr.Blocks() as self.survey:
            for _hp in self.heads:
                _t = _hp.page
            for _bp in self.bodies:
                _t = _bp.page
            _t = self.tail.page

    def load(self, survey_dict: dict):
        if ['survey_id', 'survey_theme', 'heads', 'bodies', 'tail'] in survey_dict.keys():
            try:
                self.survey_id = survey_dict['survey_id']
                self.set_theme(survey_dict['survey_theme'])
                for _hp in survey_dict['heads']:
                    self.heads.append(self._parse_page(_hp))
                for _bp in survey_dict['bodies']:
                    self.bodies.append(self._parse_page(_bp))
                self.tail = self._parse_page(survey_dict['tail'])
                self.generate_survey()
            except Exception as e:
                print(e)
                raise sError.UnableLoadSurvey(-1)
        else:
            raise sError.UnableLoadSurvey(0)

    def _parse_page(self, page_dict: dict):
        if "page_type" in page_dict.keys():
            try:
                match page_dict['page_type']:
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
            case "EMB", _:
                self.survey_theme = sThemes.SurveyTheme.EMB
