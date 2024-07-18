import logging

import pandas as pd
from survey.survey import Survey


survey = {'class_name': "113F01_AIOT物聯網智慧應用設計班",
          'survey_desc': "本問卷用以了解學生對於師資滿意度進行調查，以匿名方式提供老師日後教學上的參考，請放心填寫。",
          'teachers': ["林宜芳", "簡進士", "陳冠華", "陳柄宏", "王綉蘭", "林瓊嘉"]}

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    _survey = Survey(survey['class_name'], survey['teachers'])
    app = _survey.start_survey()
    app.launch()
