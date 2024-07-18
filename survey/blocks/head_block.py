import gradio as gr
from survey.blocks.block import Block


class HeadBlock(Block):
    def __init__(self, title: str, desc: str):
        self._desc = desc
        super().__init__(title)

    def _generate_body(self):
        with gr.Column() as _col:
            with gr.Row():
                with gr.Column(min_width=0, scale=1):
                    pass
                with gr.Column(variant="panel", scale=3, min_width=640):
                    gr.Markdown(f"# {self._title}")
                    gr.Markdown(self._desc)
                with gr.Column(min_width=0, scale=1):
                    pass
        self.body = _col


if __name__ == '__main__':
    head = HeadBlock("113F01", "描述")
    head.body.launch()
