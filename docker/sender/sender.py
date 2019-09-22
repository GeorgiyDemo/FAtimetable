"""
    Модуль sender, который ловит очередь FIFO с Redis (таблица 3)
    Запрашивает расписание с финашки и отдаёт на хост
"""

import fa_api
import requests
import redis
import time
import fa_json_module

class SendSMSClass(object):
    """
    Класс для отправки сообщения на SMS-шлюз
    """
    def __init__(self, number, sms):
        self.number = number
        self.sms = sms
        self.send_sms()

    def send_sms(self):
        print("Отправляем сообщение на "+self.number)
        print("Сообщение: "+self.sms)
        sms_list = self.sms.split("\a")
        sms_list.pop(-1)
        for sms in sms_list:
            r = requests.get("http://77.37.132.120:5554/SendSMS/user=&password=123456&phoneNumber="+self.number+"&msg="+sms)
            print(sms+"\n-> "+r.text)
            time.sleep(1)
        time.sleep(30)

class MainProcessingClass():
    def __init__(self, number, group_id, group_name, session_token):

        self.session_token = session_token
        self.number = number
        self.group_id = group_id
        self.group_name = group_name
        self.processing()
        
    def processing(self):
        fa = fa_api.TTClass(self.session_token, self.group_id)
        obj = fa_json_module.JSONProcessingClass(self.group_name, fa.tt)
        #Отправляем по SMS
        SendSMSClass(self.number, obj.outstring)
        
