from survey.blocks.block import Block


class InputBlock(Block):
    def __init__(self, title: str, must: bool):
        self.must = must
        self.result = []
        super().__init__(title)

    def get_result(self):
        return self.result

    def get_input_components(self):
        pass
