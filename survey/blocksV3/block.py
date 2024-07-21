import gradio as gr


class Block:
    """
    基礎方塊，問卷組成最基本的元素，所有方塊元素的父類別
    """
    def __init__(self):
        self.body: gr.Row

    def _generate_body(self):
        pass
