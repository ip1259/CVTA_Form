import uvicorn

import survey.surveys.survey as sr
from . import survey_client as sc
from fastapi import FastAPI
import os
import gradio as gr


class SurveyServer:
    def __init__(self):
        """

        """
        # clients: 儲存用戶端資料為dict型別,key值為一tuple，(Survey, ip-address-string)
        self.clients: dict[(sr.Survey, str), sc.SurveyClient] = {}
        self.survey: list[sr.Survey] = []

    def load_surveys(self):
        _path = os.getcwd()
        _path = os.path.join(_path, "Surveys")
        _files = os.listdir(_path)
        print(_files)
        _survey_files = []
        for _f in _files:
            if _f.split('.')[-1] == "sr":
                print(os.path.join(_path, _f))
                _survey_files.append(os.path.join(_path, _f))
        for _sf in _survey_files:
            _tmp = sr.Survey(self)
            _tmp.set_survey(_sf)
            self.survey.append(_tmp)

    def start_server(self):
        app = FastAPI()
        for s in self.survey:
            app = gr.mount_gradio_app(app, s.survey, path="/"+s.survey_id)
        uvicorn.run(app, host='0.0.0.0', port=7860)
