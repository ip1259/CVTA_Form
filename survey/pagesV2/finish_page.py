from survey.pagesV2 import custom_page
from survey.network import survey_server as server
from survey.surveys import survey


class FinishPage(custom_page.CustomPage):
    def __init__(self,
                 parent_server: server.SurveyServer,
                 parent_survey: survey.Survey):
        _BLOCK_DICTS: list[dict] = [{
            'block_type': "finish"
        }]
        super().__init__(parent_server, parent_survey)
        self.load(_BLOCK_DICTS)


if __name__ == '__main__':
    import gradio as gr

    with gr.Blocks() as demo:
        tp = FinishPage(None, None)
    demo.launch()
