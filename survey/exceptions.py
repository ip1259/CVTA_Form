class UnableParseBlock(Exception):
    def __init__(self, err_code: int, par_str: str = None):
        msg = ""
        match err_code:
            case 0:
                msg = "無法解析Block Json,缺少鍵值'block_type'"
            case 1:
                msg = "無法解析Block Json,無法配對block type"
            case 2:
                msg = "無法解析Block Json,缺少參數"
            case 3:
                msg = f"無法解析Block Json,參數{par_str}型別錯誤"
            case _:
                msg = "未知錯誤"
        super().__init__(msg)


class UnableParsePage(Exception):
    def __init__(self, err_code: int, par_str: str = None):
        msg = ""
        match err_code:
            case 0:
                msg = "無法解析Page Json,缺少鍵值'page_type'"
            case 1:
                msg = "無法解析Page Json,無法配對page type"
            case 2:
                msg = "無法解析Page Json,缺少參數"
            case 3:
                msg = f"無法解析Page Json,參數{par_str}型別錯誤"
            case _:
                msg = "未知錯誤"
        super().__init__(msg)


class UnableLoadSurvey(Exception):
    def __init__(self, err_code: int):
        msg = ""
        match err_code:
            case 0:
                msg = "無法載入 Survey Json,缺少必要鍵值:'survey_id', 'survey_theme', 'heads', 'bodies', 'tail'"
            case _:
                msg = "未知錯誤"
        super().__init__(msg)
