"""
    Модуль sender, который ловит очередь FIFO с Redis (таблица 3)
    Запрашивает расписание с финашки и отдаёт на хост
"""

import time
import requests

class SendSMSClass(object):
    """
    Класс для отправки сообщения на SMS-шлюз
    """

    def __init__(self, number, sms, config):
        self.number = number
        self.sms = sms
        self.config = config
        self.send_sms()

    #TODO SENDER ПЕРЕДЕЛАТЬ ОТПРАВКУ SMS
    def send_sms(self):
        print("Отправляем сообщение на " + self.number+"..")
        for s in self.sms:
            try:
                requests.get(
                "http://"+self.config["gsm_url"]+"/SendSMS/user=&password="+self.config["gsm_password"]+"&phoneNumber=" + self.number + "&msg=" + s)
            except:
                raise Exception('GSM server', 'GSM server exception')
            time.sleep(1)

        time.sleep(self.config["SMS_TIME_SLEEP"])


