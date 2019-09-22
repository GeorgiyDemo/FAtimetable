import requests
import yaml

class FaClass(object):

    def __init__(self, user_data, datatime):
        
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)'
        }
        self.datatime = datatime
        self.token = user_data[0]
        self.user_id = user_data[1]
        self.get_timetable_byday()

    def get_timetable_byday(self):
        """
        Получение информации о расписании на конкретную дату date
        - Принимает дату date в формате 01.01.2019
        """
        raw_data = "UserId="+str(self.user_id)+"&Token="+self.token+"&Date="+self.datatime
        r = requests.post("https://portal.fa.ru/mGosvpoAccount/TimeTable", data=raw_data, headers=self.headers).json()
        self.tt = r