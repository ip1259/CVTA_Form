from .input_block import InputBlock
import gradio as gr


class SuggestionBlock(InputBlock):
    def __init__(self, title: str, desc: str = "",  must: bool = False):
        super().__init__(title, desc, must)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(variant="panel", min_width=640):
                gr.Markdown(f"## {self.title}")
                if self.desc != "":
                    gr.Markdown(f'<div align="left"> *{self.desc}*</div>')
                _suggestion = gr.TextArea(lines=5, container=False, show_label=False)
                self.interactions.append(_suggestion)

    # def set_interactive_triggered(self, user_store: gr.State):
    #     def set_result(value, _user_store):
    #         _user_store['results'][self.interactions[0]] = (self.title, value)
    #         return _user_store
    #
    #     self.interactions[0].change(fn=set_result, inputs=[self.interactions[0], user_store], outputs=user_store)
