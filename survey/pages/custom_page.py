import json

import gradio as gr

from survey.blocks import BlockParser, Block
from survey.pages import Page


class CustomPage(Page):
    def __init__(self):
        super().__init__()

    def _generate_page(self):
        with gr.Row() as self.page:
            for _b in self.page_blocks:
                self.page.add(_b.body)

    def load(self, block_dicts: list[dict]):
        with gr.Row() as self.page:
            with gr.Column():
                for _block_dict in block_dicts:
                    self.page_blocks.append(BlockParser.parse_block(_block_dict))

    def reload_block_dicts(self):
        pass

    def load_json_file(self, file_path):
        """
        載入描述Page內容的Json檔以生成自定義Page
        :param file_path:
        :return: None
        """
        self.page_blocks: list[Block] = []
        with open(file_path, 'r', encoding='utf8') as _f:
            block_dicts: list[dict] = json.load(_f)
            self.load(block_dicts)

    def load_json_string(self, j_str: str):
        self.page_blocks: list[Block] = []
        block_dicts: list[dict] = json.loads(j_str)
        self.load(block_dicts)

    def set_page_interactive(self):
        pass


if __name__ == '__main__':
    import os
    cp = CustomPage()

    with gr.Blocks() as demo:
        cp.load_json_file(os.path.join("../../test_file", "custom_test.json"))
    demo.launch()
