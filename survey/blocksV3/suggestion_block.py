from .input_block import InputBlock
import gradio as gr


class SuggestionBlock(InputBlock):
    def __init__(self, title: str,  must: bool = False):
        super().__init__(title, must)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(variant="panel", min_width=640):
                gr.Markdown(f"## {self.title}")
                _suggestion = gr.TextArea(lines=5, container=False, show_label=False)
                self.interactions.append(_suggestion)

    def get_input_components(self):
        return self.interactions

    # def set_interactive_triggered(self, user_store: gr.State):
    #     def set_result(value, _user_store):
    #         _user_store['results'][self.interactions[0]] = (self.title, value)
    #         return _user_store
    #
    #     self.interactions[0].change(fn=set_result, inputs=[self.interactions[0], user_store], outputs=user_store)
