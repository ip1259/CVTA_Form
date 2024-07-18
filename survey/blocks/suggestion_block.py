from survey.blocks.input_block import InputBlock
import gradio as gr


class SuggestionBlock(InputBlock):
    def __init__(self, title: str, parent, must: bool = False):
        self.suggestion: gr.TextArea | None = None
        super().__init__(title, must, parent)
        self._generate_body()

    def _generate_body(self):
        def set_result(value, request: gr.Request):
            if request:
                print(request.client.host)
                _ip = request.client.host
                self.parent.clients[_ip].response.set_response(self, value)

        with gr.Column() as _col:
            with gr.Row():
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="panel", scale=3, min_width=640):
                    gr.Markdown(f"## {self.title}")
                    self.suggestion = gr.TextArea(lines=5, container=False, show_label=False)

                with gr.Column(min_width=0, scale=1):
                    pass
            self.suggestion.change(set_result, [self.suggestion])
        self.body = _col

    def get_input_components(self):
        return [self.suggestion]
