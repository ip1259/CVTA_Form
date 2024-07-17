from survey.blocks.block import Block
import gradio as gr


class SuggestionBlock(Block):
    def __init__(self, title: str):
        self.suggestion = None
        super().__init__(title)

    def _generate_body(self):
        with gr.Blocks() as _block:
            with gr.Row():
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="panel", scale=3, min_width=640):
                    gr.Markdown(f"## {self._title}")
                    self.suggestion = gr.TextArea(lines=5, container=False, show_label=False)

                with gr.Column(min_width=0, scale=1):
                    pass
        self.body = _block
