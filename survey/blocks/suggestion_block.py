from survey.blocks.input_block import InputBlock
import gradio as gr


class SuggestionBlock(InputBlock):
    def __init__(self, title: str,
                 parent_server, parent_survey,
                 must: bool = False):
        self.suggestion: gr.TextArea | None = None
        super().__init__(title, must, parent_survey, parent_server)
        self._generate_body()

    def _generate_body(self):
        with gr.Row() as self.body:
            with gr.Column(min_width=0, scale=1):
                pass
            with gr.Column(variant="panel", scale=3, min_width=640):
                gr.Markdown(f"## {self.title}")
                self.suggestion = gr.TextArea(lines=5, container=False, show_label=False)

            with gr.Column(min_width=0, scale=1):
                pass

    def get_input_components(self):
        return [self.suggestion]

    def set_interactive_triggered(self):
        def set_result(value, request: gr.Request):
            if request:
                # print("Suggestion changed {0}".format(value), request.client.host)
                _ip = request.client.host
                self.set_result(_ip, value)

        self.suggestion.change(set_result, [self.suggestion])
