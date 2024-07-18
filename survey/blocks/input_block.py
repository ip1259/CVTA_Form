from survey.blocks.block import Block


class InputBlock(Block):

    def __init__(self, title: str, must: bool, parent):
        self.parent = parent
        self.must = must
        super().__init__(title)
        self.result = 0

    def get_result(self, ip: str):
        return self.parent.clients[ip].response.response[self][2]

    def get_input_components(self):
        pass

    def get_response(self, ip: str):
        return self.title, self.get_result(ip)
