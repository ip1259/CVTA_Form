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
        def set_result(value, request: gr.Request):
            if request:
                # print(request.client.host)
                _ip = request.client.host
                self.set_result(_ip, value)

            with gr.Row() as _row:
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="panel", scale=3, min_width=640):
                    gr.Markdown(f"## {self.title}")
                    with gr.Row():
                        gr.Text(self._min_score_desc, container=False, show_label=False, text_align='right',
                                max_lines=1, min_width=0)
                        self.score = gr.Radio(list(range(1, self._max_score + 1)), show_label=False, container=False,
                                              min_width=75 * self._max_score, type="value")
                        gr.Text(self._max_score_desc, container=False, show_label=False, max_lines=1, min_width=0)
                with gr.Column(min_width=0, scale=1):
                    pass
                self.score.change(set_result, [self.score])

            self.body = _row

    def get_input_components(self):
        # print([self.score])
        return [self.score]
