from .block import Block
from .interactive_block import InteractiveBlock
from .input_block import InputBlock
from .head_block import HeadBlock
from .finish_block import FinishBlock
from .score_block import ScoreBlock
from .suggestion_block import SuggestionBlock
from .tail_btn_block import TailButtonBlock
from survey.exceptions import UnableParseBlock


class BlockParser:
    @staticmethod
    def parse_block(block_dict: dict):
        if "block_type" in block_dict.keys():
            try:
                match block_dict['block_type']:
                    case "tail_btn":
                        return tail_btn_block.TailButtonBlock(block_dict['body_count'])
                    case "head":
                        return head_block.HeadBlock(block_dict['title'], block_dict['desc'])
                    case "finish":
                        _fb = finish_block.FinishBlock()
                        if "title" in block_dict.keys():
                            if not isinstance(block_dict['title'], str):
                                raise UnableParseBlock(3, f"{block_dict['block_type']}-'title'")
                            _fb.title = block_dict['title']
                        return _fb
                    case "score":
                        _sb = score_block.ScoreBlock(block_dict['title'])
                        if "must" in block_dict.keys():
                            if not isinstance(block_dict['must'], bool):
                                raise UnableParseBlock(3, f"{block_dict['block_type']}-'must'")
                            _sb.must = block_dict['must']
                        if "max_score" in block_dict.keys():
                            if not isinstance(block_dict['max_score'], int):
                                raise UnableParseBlock(3, f"{block_dict['block_type']}-'max_score'")
                            _sb.set_max_score(block_dict['max_score'])
                        if "max_score_desc" in block_dict.keys():
                            if not isinstance(block_dict['max_score_desc'], str):
                                raise UnableParseBlock(3, f"{block_dict['block_type']}-'max_score_desc'")
                            _sb.set_max_score_desc(block_dict['max_score_desc'])
                        if "min_score_desc" in block_dict.keys():
                            if not isinstance(block_dict['min_score_desc'], str):
                                raise UnableParseBlock(3, f"{block_dict['block_type']}-'min_score_desc'")
                            _sb.set_min_score_desc(block_dict['min_score_desc'])
                        return _sb
                    case "suggestion":
                        _sb = suggestion_block.SuggestionBlock(block_dict['title'])
                        if "must" in block_dict.keys():
                            if not isinstance(block_dict['must'], bool):
                                raise UnableParseBlock(3, f"{block_dict['block_type']}-'must'")
                            _sb.must = block_dict['must']
                        return _sb
                    case _:
                        raise UnableParseBlock(1)
            except Exception as e:
                print(e)
                raise UnableParseBlock(2)
        else:
            raise UnableParseBlock(0)
