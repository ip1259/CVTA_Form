from survey.blocks.input_block import InputBlock
import gradio as gr


class ScoreBlock(InputBlock):
    def __init__(self, title: str, must: bool = True, max_score: int = 5, min_score_desc: str = "非常不滿意", max_score_desc: str = "非常滿意"):
        self.score: gr.Radio | None = None
        self._max_score = max_score
        self._min_score_desc = min_score_desc
        self._max_score_desc = max_score_desc
        super().__init__(title, must)

    def _generate_body(self):
        with gr.Column() as _col:
            with gr.Row():
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="panel", scale=3, min_width=640):
                    gr.Markdown(f"## {self._title}")
                    with gr.Row():
                        gr.Text(self._min_score_desc, container=False, show_label=False, text_align='right', max_lines=1, min_width=0)
                        self.score = gr.Radio(list(range(1, self._max_score+1)), show_label=False, container=False, min_width=75*self._max_score)
                        gr.Text(self._max_score_desc, container=False, show_label=False, max_lines=1, min_width=0)
                with gr.Column(min_width=0, scale=1):
                    pass
        self.body = _col

    def get_result(self):
        if self.score is not None:
            return self.score.value
        return None
