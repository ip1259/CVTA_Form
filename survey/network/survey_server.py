import survey.surveys.survey as sr
import survey_client as sc


class SurveyServer:
    def __init__(self):
        """

        """
        # clients: 儲存用戶端資料為dict型別,key值為一tuple，(Survey, ip-address-string)
        self.clients: dict[(sr.Survey, str), sc.SurveyClient] = {}
        self.survey: list[sr.Survey] = []


if __name__ == '__main__':
    print("test")
