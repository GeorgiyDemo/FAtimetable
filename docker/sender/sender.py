"""
    Модуль sender, который ловит очередь FIFO с Redis (таблица 3)
    Запрашивает расписание с финашки и отдаёт на хост
"""

import fa_api
import requests
import redis
import time
import datetime
import fa_json_module

def get_date_now():
    
    """
    Метод для получения текущей даты
    в формате 01.01.2019
    """
    today = datetime.date.today()
    return today.strftime("%d.%m.%Y")

class SendSMSClass(object):
    """
    Класс для отправки сообщения на SMS-шлюз
    """
    def __init__(self, number, sms):
        self.number = number
        self.sms = sms
        self.send_sms()

    def send_sms(self):
        r = requests.get("http://77.37.132.120:5554/SendSMS/user=&password=123456&phoneNumber="+self.number+"&msg="+self.sms)
        time.sleep(30)

class MainProcessingClass():
    def __init__(self, number, group_id, user_data):

        self.user_data = user_data
        self.number = number
        self.group_id = group_id
        self.processing()
        
    def processing(self):
        fa = fa_api.FaClass(self.user_data, get_date_now())
        #Возвращаем какой-нибудь объект отсюда
        fa_json_module.JSONProcessingClass(fa.tt)
        #

