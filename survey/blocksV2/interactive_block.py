from survey.blocksV2.block import Block


class InteractiveBlock(Block):
    def __init__(self, title: str, parent_survey, parent_server):
        self.server = parent_server
        super().__init__(title, parent_survey)

    def set_interactive_triggered(self):
        pass
