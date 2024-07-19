from survey.surveys.standard_survey import StandardSurvey


survey = {'class_name': "113F01_AIOT物聯網智慧應用設計班",
          'survey_id': "113F01",
          'has_ta': False,
          'survey_desc': "本問卷用以了解學生對於師資滿意度進行調查，以匿名方式提供老師日後教學上的參考，請放心填寫。",
          'teachers': ["林宜芳", "簡進士", "陳冠華", "陳柄宏", "王綉蘭", "林瓊嘉"]}

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    _survey = StandardSurvey(survey['class_name'], survey['teachers'], survey_id=survey['survey_id'], has_ta=survey['has_ta'])
    app = _survey.start_survey()
    app.launch(server_name="0.0.0.0")
