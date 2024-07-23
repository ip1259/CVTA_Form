from .page import Page
from .custom_page import CustomPage
from .head_page import HeadPage
from .finish_page import FinishPage
from .tail_btn_page import TailButtonPage
from .teacher_page import TeacherPage
from .employment_page import EmploymentPage
from .ta_page import TAPage
from survey.exceptions import UnableParsePage


class PageParser:
    @staticmethod
    def parse_page(page_dict: dict):
        if "page_type" in page_dict.keys():
            try:
                match page_dict['page_type']:
                    case "tail_btn":
                        _tp = TailButtonPage(page_dict['body_count'])
                        _tp.load_self()
                        return _tp
                    case "head":
                        _hp = HeadPage(page_dict['title'])
                        if "desc" in page_dict.keys():
                            if not isinstance(page_dict['desc'], str):
                                raise UnableParsePage(3, f"{page_dict['page_type']}-'desc'")
                            _hp.set_desc(page_dict['desc'])
                        _hp.load_self()
                        return _hp
                    case "finish":
                        _fp = FinishPage()
                        _fp.load_self()
                        return _fp
                    case "teacher":
                        _tp = TeacherPage(page_dict['teacher'])
                        if "max_score" in page_dict.keys():
                            if not isinstance(page_dict['max_score'], int):
                                raise UnableParsePage(3, f"{page_dict['page_type']}-'max_score'")
                            _tp.set_max_score(page_dict['max_score'])
                        if "desc" in page_dict.keys():
                            if not isinstance(page_dict['desc'], str):
                                raise UnableParsePage(3, f"{page_dict['page_type']}-'desc'")
                            _tp.set_desc(page_dict['desc'])
                        _tp.load_self()
                        return _tp
                    case "ta":
                        _tp = TAPage()
                        if "max_score" in page_dict.keys():
                            if not isinstance(page_dict['max_score'], int):
                                raise UnableParsePage(3, f"{page_dict['page_type']}-'max_score'")
                            _tp.set_max_score(page_dict['max_score'])
                        _tp.load_self()
                        return _tp
                    case "employment":
                        _ep = EmploymentPage()
                        _ep.load_self()
                        return _ep
                    case "custom":
                        _cp = CustomPage()
                        _cp.load(page_dict['block_dicts'])
                        return _cp
                    case _:
                        raise UnableParsePage(1)
            except Exception as e:
                print(e)
                raise UnableParsePage(2)
        else:
            raise UnableParsePage(0)
