"""
Пример работы с модулем fa_api
"""
import fa_api
import datetime
import requests

class SendSMSClass(object):

    def __init__(self, number, sms):
        self.number = number
        self.sms = sms
        self.send_sms()

    def send_sms(self):
        
        r = requests.get("http://77.37.132.120:5554/SendSMS/user=&password=123456&phoneNumber="+self.number+"&msg="+self.sms)


def get_date_tomorrow():
    
    """
    Метод для получения завтрашнего дня
    """

    today = datetime.date.today()
    future = today + datetime.timedelta(days=1)
    return future.strftime("%d.%m.%Y")


def main():

    #Создаём объект
    fa = fa_api.FaClass()

    #Обращаемся к методу get_group
    group = fa.get_group()
    print(group)

    #Получаем расписание на завтра
    tt = fa.get_timetable_byday(get_date_tomorrow())
    print(tt)

if __name__ == "__main__":
    SendSMSClass("+79999645590","Кошкочасы у Демы ;3")