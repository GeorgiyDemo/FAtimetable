"""
    Модуль sender, который ловит очередь FIFO с Redis (таблица 3)
    Запрашивает расписание с финашки и отдаёт на хост
"""

import fa_api
import requests
import redis
import time
import datetime

class SendSMSClass(object):

    def __init__(self, number, sms):
        self.number = number
        self.sms = sms
        self.send_sms()

    def send_sms(self):
        r = requests.get("http://77.37.132.120:5554/SendSMS/user=&password=123456&phoneNumber="+self.number+"&msg="+self.sms)
        time.sleep(10)

def get_date_tomorrow():
    
    """
    Метод для получения завтрашнего дня
    """

    today = datetime.date.today()
    future = today + datetime.timedelta(days=1)
    return future.strftime("%d.%m.%Y")

class MainProcessingClass():
    def __init__(self, number, group_id):
       
        self.number = number
        self.group_id = group_id
        self.processing()
        
    def processing(self):
        #Создаём объект
        fa = fa_api.FaClass()
        
        #Обращаемся к методу get_group
        group = fa.get_group()
        print(group)
        
        #Получаем расписание на завтра
        tt = fa.get_timetable_byday(get_date_tomorrow())
        print(tt)

#TODO Авторизация в личном кабинете финашки при первом запуске (??) 
# ВОЗМОЖНО RQ-WORKER НЕ ДАСТ ТАК СДЕЛАТЬ