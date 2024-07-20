from survey.blocksV2 import interactive_block


class InputBlock(interactive_block.InteractiveBlock):

    def __init__(self, title: str, must: bool, parent_survey, parent_server):
        self.must = must
        super().__init__(title, parent_survey, parent_server)
        self.result = 0

    def get_result(self, ip: str):
        return self.server.clients[(self.parent_survey, ip)].response.response[self][2]

    def set_result(self, ip: str, value):
        self.server.clients[(self.parent_survey, ip)].response.set_response(self, value)

    def get_input_components(self):
        pass

    def get_response(self, ip: str):
        return self.title, self.get_result(ip)

    def set_interactive_triggered(self):
        pass
