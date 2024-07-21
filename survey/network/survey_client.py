import os
import survey.blocks.input_block as input_block


class SurveyClient:
    def __init__(self, ip: str, parent_survey):
        self.ip = ip
        self.parent = parent_survey
        self.response = SurveyResponse(parent_survey)
        self.cur_body_index: int = 0
        self.body_visible_states: list[bool] = [r.visible for r in self.parent.get_rows_in_bodies()]

    def save_response(self):
        _path = os.getcwd()
        _path = os.path.join(_path, "responses")
        if not os.path.exists(_path):
            os.mkdir(_path)
        _path = os.path.join(_path, self.parent.survey_id)
        if not os.path.exists(_path):
            os.mkdir(_path)
        from joblib import dump
        dump([i for i in self.response.response.values()], os.path.join(_path, self.ip.split('.')[-1] + ".rep"))
        # example: list[tuple[str, bool, str | int | float]] = load("[WorkDir]/responses/[SurveyID]/[IPv4最後一位.rep]")
        #
        # _wb = None
        # _path = os.path.join(_path, self.parent.survey_id + ".xlsx")
        # if not os.path.exists(_path):
        #     _wb = openpyxl.Workbook()
        #     _wb.create_sheet("表單回覆")
        #     _wb.remove_sheet(_wb["Sheet"])
        #     _ws = _wb["表單回覆"]
        #     _titles = ["IP"]
        #     _titles.extend([_t[0] for _t in self.response.response.values()])
        #     _ws.append(_titles)
        #     _wb.save(_path)
        # _wb = openpyxl.load_workbook(_path)
        # _response = [self.ip]
        # _response.extend([_t[2] for _t in self.response.response.values()])
        # for i, r in enumerate(_response):
        #     if r is None:
        #         _response[i] = ""
        # _ws = _wb["表單回覆"]
        # _ws.append(_response)
        # _wb.save(_path)

    def set_cur_body(self, index: int):
        self.cur_body_index = index
        self.cur_body_index = min(self.cur_body_index, len(self.body_visible_states) - 1)
        self.cur_body_index = max(self.cur_body_index, 0)
        for _i in range(len(self.body_visible_states)):
            if _i == self.cur_body_index:
                self.body_visible_states[_i] = True
            else:
                self.body_visible_states[_i] = False


class SurveyResponse:
    def __init__(self, parent_survey):
        self.parent = parent_survey
        # example self.response[an InputBlock Object as KEY] = (Question, Must Answer Or Not, Value)
        self.response: dict[input_block.InputBlock, tuple[str, bool, str | int | float]] = {}
        self.init_response()

    def init_response(self):
        _inputs = self.parent.get_survey_input_components()
        for i in _inputs:
            self.set_response(i, None)

    def set_response(self, block: input_block.InputBlock, value):
        self.response[block] = (block.title, block.must, value)
