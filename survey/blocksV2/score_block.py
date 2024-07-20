from survey.blocksV2.input_block import InputBlock
from survey.network import survey_server as server
from survey.surveys import survey
import gradio as gr


class ScoreBlock(InputBlock):
    def __init__(self,
                 title: str, parent_server: server.SurveyServer, parent_survey: survey.Survey,
                 must: bool = True, max_score: int = 5,
                 min_score_desc: str = "非常不滿意",
                 max_score_desc: str = "非常滿意"):
        self.score: gr.Radio | None = None
        self._max_score = max_score
        self._min_score_desc = min_score_desc
        self._max_score_desc = max_score_desc
        super().__init__(title, must, parent_survey, parent_server)
        self._generate_body()

    def _generate_body(self):

        with gr.Row() as self.body:
            gr.Column(min_width=0, scale=1)

            with gr.Column(variant="panel", scale=3, min_width=640):
                gr.Markdown(f"## {self.title}")
                with gr.Row():
                    with gr.Column(scale=3, min_width=70):
                        gr.Markdown(f'## <div align="right">{self._min_score_desc}</div>', show_label=False)
                    with gr.Column(scale=10):
                        with gr.Row():
                            gr.Column(scale=1, min_width=0)
                            self.score = gr.Radio(list(range(1, self._max_score + 1)), show_label=False,
                                                  container=False, type="value", min_width=self._max_score*69)
                            gr.Column(scale=1, min_width=0)
                    with gr.Column(scale=3, min_width=70):
                        gr.Markdown(f'## <div align="right">{self._max_score_desc}</div>', show_label=False)

            gr.Column(min_width=0, scale=1)

    def get_input_components(self):
        # print([self.score])
        return [self.score]

    def set_max_score(self, score: int):
        self._max_score = score

    def set_max_score_desc(self, desc: str):
        self._max_score_desc = desc

    def set_min_score_desc(self, desc: str):
        self._min_score_desc = desc

    def set_input_changed(self):
        def set_result(value, request: gr.Request):
            if request:
                # print("Radio selected : {0}".format(value), request.client.host)
                _ip = request.client.host
                self.set_result(_ip, value)
        self.score.change(set_result, [self.score])
