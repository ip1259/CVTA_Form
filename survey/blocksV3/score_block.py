from .input_block import InputBlock
import gradio as gr


class ScoreBlock(InputBlock):
    def __init__(self, title: str, must: bool = True, max_score: int = 5,
                 min_score_desc: str = "非常不滿意", max_score_desc: str = "非常滿意"):
        self._max_score = max_score
        self._min_score_desc = min_score_desc
        self._max_score_desc = max_score_desc
        super().__init__(title, must)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(variant="panel", min_width=640):
                gr.Markdown(f"## {self.title}")
                with gr.Row():
                    with gr.Column(scale=3, min_width=70):
                        gr.Markdown(f'## <div align="right">{self._min_score_desc}</div>', show_label=False)
                    with gr.Column(scale=10):
                        with gr.Row():
                            gr.Column(scale=1, min_width=0)
                            _radio = gr.Radio(list(range(1, self._max_score + 1)), show_label=False,
                                              container=False, type="value", min_width=self._max_score * 75)
                            self.interactions.append(_radio)
                            gr.Column(scale=1, min_width=0)
                    with gr.Column(scale=3, min_width=70):
                        gr.Markdown(f'## <div align="right">{self._max_score_desc}</div>', show_label=False)

    def set_max_score(self, score: int):
        self._max_score = score

    def set_max_score_desc(self, desc: str):
        self._max_score_desc = desc

    def set_min_score_desc(self, desc: str):
        self._min_score_desc = desc

    # def set_interactive_triggered(self, user_store: gr.State):
    #     def set_result(value, _user_store):
    #         _user_store['results'][self.interactions[0]] = (self.title, value)
    #         return _user_store
    #
    #     self.interactions[0].change(fn=set_result, inputs=[self.interactions[0], user_store], outputs=user_store)
