"""
    Модуль sender, который ловит очередь FIFO с Redis (таблица 3)
    Запрашивает расписание с финашки и отдаёт на хост
"""

import time

import fa_api
import fa_json_module
import requests


class SendSMSClass(object):
    """
    Класс для отправки сообщения на SMS-шлюз
    """

    def __init__(self, number, sms, config):
        self.number = number
        self.config = config
        self.sms = sms
        self.send_sms()

    def send_sms(self):
        print("Отправляем сообщение на " + self.number+"..")
        sms_list = self.sms.split("\a")
        sms_list.pop(-1)
        for sms in sms_list:
            r = requests.get(
                "http://"+self.config["gsm_url"]+"/SendSMS/user=&password="+self.config["gsm_password"]+"&phoneNumber=" + self.number + "&msg=" + sms)
            print(sms + "\n-> " + r.text)
            time.sleep(1)

        time.sleep(self.config["SMS_TIME_SLEEP"])


class MainProcessingClass():
    def __init__(self, number, group_id, group_name, session_token, config):

        self.config = config
        self.session_token = session_token
        self.number = number
        self.group_id = group_id
        self.group_name = group_name
        self.processing()

    def processing(self):
        fa = fa_api.TTClass(self.session_token, self.group_id, self.config)
        if fa.tt != {}:
            obj = fa_json_module.JSONProcessingClass(self.group_name, fa.tt)
            SendSMSClass(self.number, obj.outstring, self.config)
        else:
            print(self.number, self.group_name, "-> пар неть")