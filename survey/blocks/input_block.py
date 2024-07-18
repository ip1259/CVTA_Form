from survey.blocks.block import Block


class InputBlock(Block):
    def __init__(self, title: str, must: bool):
        self.must = must
        super().__init__(title)

    def get_result(self):
        pass

    def get_input_components(self):
        pass
