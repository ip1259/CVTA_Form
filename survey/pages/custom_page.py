import json

import gradio as gr

from survey.blocks import *
from survey.pages import page
from survey import exceptions as sError


class CustomPage(page.Page):
    def __init__(self, parent_server, parent_survey):
        super().__init__(parent_server, parent_survey)

    def _generate_page(self):
        with gr.Row() as self.page:
            for _b in self.page_blocks:
                self.page.add(_b.body)

    def load(self, block_dicts: list[dict]):
        with gr.Row() as self.page:
            with gr.Column():
                for _block_dict in block_dicts:
                    self.page_blocks.append(self._parse_block(_block_dict))

    def load_json_file(self, file_path):
        """
        載入描述Page內容的Json檔以生成自定義Page
        :param file_path:
        :return: None
        """
        self.page_blocks = []
        with open(file_path, 'r', encoding='utf8') as _f:
            block_dicts: list[dict] = json.load(_f)
            self.load(block_dicts)

    def load_json_string(self, j_str: str):
        self.page_blocks = []
        block_dicts: list[dict] = json.loads(j_str)
        self.load(block_dicts)

    def _parse_block(self, block_dict: dict):
        if "block_type" in block_dict.keys():
            try:
                match block_dict['block_type']:
                    case "tail_btn":
                        return tail_btn_block.TailButtonBlock(self.parent, self.server)
                    case "head":
                        return head_block.HeadBlock(block_dict['title'], block_dict['desc'], self.parent)
                    case "finish":
                        _fb = finish_block.FinishBlock(self.parent)
                        if "title" in block_dict.keys():
                            if not isinstance(block_dict['title'], str):
                                raise sError.UnableParseBlock(3, f"{block_dict['block_type']}-'title'")
                            _fb.title = block_dict['title']
                        return _fb
                    case "score":
                        _sb = score_block.ScoreBlock(block_dict['title'], self.server, self.parent)
                        if "must" in block_dict.keys():
                            if not isinstance(block_dict['must'], bool):
                                raise sError.UnableParseBlock(3, f"{block_dict['block_type']}-'must'")
                            _sb.must = block_dict['must']
                        if "max_score" in block_dict.keys():
                            if not isinstance(block_dict['max_score'], int):
                                raise sError.UnableParseBlock(3, f"{block_dict['block_type']}-'max_score'")
                            _sb.set_max_score(block_dict['max_score'])
                        if "max_score_desc" in block_dict.keys():
                            if not isinstance(block_dict['max_score_desc'], str):
                                raise sError.UnableParseBlock(3, f"{block_dict['block_type']}-'max_score_desc'")
                            _sb.set_max_score_desc(block_dict['max_score_desc'])
                        if "min_score_desc" in block_dict.keys():
                            if not isinstance(block_dict['min_score_desc'], str):
                                raise sError.UnableParseBlock(3, f"{block_dict['block_type']}-'min_score_desc'")
                            _sb.set_min_score_desc(block_dict['min_score_desc'])
                        return _sb
                    case "suggestion":
                        _sb = suggestion_block.SuggestionBlock(block_dict['title'], self.server, self.parent)
                        if "must" in block_dict.keys():
                            if not isinstance(block_dict['must'], bool):
                                raise sError.UnableParseBlock(3, f"{block_dict['block_type']}-'must'")
                            _sb.must = block_dict['must']
                        return _sb
                    case _:
                        raise sError.UnableParseBlock(1)
            except Exception as e:
                print(e)
                raise sError.UnableParseBlock(2)
        else:
            raise sError.UnableParseBlock(0)

    def set_page_interactive(self):
        for _b in self.page_blocks:
            if isinstance(_b, interactive_block.InteractiveBlock):
                _b.set_interactive_triggered()


if __name__ == '__main__':
    import os
    cp = CustomPage(None, None)

    with gr.Blocks() as demo:
        cp.load_json_file(os.path.join("../../test_file", "custom_test.json"))
    demo.launch()
