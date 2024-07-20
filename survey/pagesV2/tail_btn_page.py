from survey.pagesV2 import custom_page


class TailButtonPage(custom_page.CustomPage):
    def __init__(self,
                 parent_server,
                 parent_survey):
        _BLOCK_DICTS: list[dict] = [{
            'block_type': "tail_btn"
        }]
        super().__init__(parent_server, parent_survey)
        self.load(_BLOCK_DICTS)


if __name__ == '__main__':
    pass
