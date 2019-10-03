"""
Модуль для заполнения очереди FIFO в назначенное время
"""

import datetime
import time

import fa_api_module
import fa_json_module

import redis
import requests
import rq
import yaml

class GetSettingsClass(object):
    """
    Класс для чтения настроек с yaml
    """
    def __init__(self):
        self.get_settings()
    
    def get_settings(self):
        with open("./yaml/settings.yml", 'r') as stream:
            self.config = yaml.safe_load(stream)

class FATokenClass(object):
    """
    Класс для получения токена и id пользователя ИОП 

    - Авторизуется с логином/паролем в settings.yaml
    - В self.user_data отдаёт tuple с токеном и id пользователя
    """

    def __init__(self, config):
        self.config = config
        self.get_token_site()

    def get_token_site(self):
        session = requests.session()
        session.cookies['ASP.NET_SessionId'] = self.get_cookies_site()
        self.user_token = session

    def get_cookies_site(self):
        """
        Получение cookies по логину и паролю на сайте ИОП
        """
        session = requests.session()
        response = session.post(self.config['url']+'/CoreAccount/LogOn',
                                data={'Login': self.config["login"], 'Pwd': self.config["password"]},
                                headers=self.config["headers"], allow_redirects=True)
        data = session.cookies['ASP.NET_SessionId']
        session.close()
        if response.url == self.config['url']+'/CoreAccount/Portal':
            return data
        else:
            raise Exception("Can't login into IOP", data)


r_number2group = redis.Redis(host='redis', port=6379, decode_responses=True, db=1)
r_group2id = redis.Redis(host='redis', port=6379, decode_responses=True, db=2)
r_id2timetable = redis.Redis(host='redis', port=6379, decode_responses=True, db=4)

# Подключение для создания очереди в Redis с помощью python-rq
queue = rq.Queue('sender-tasks', connection=redis.Redis.from_url('redis://redis:6379/3'))

s_obj = GetSettingsClass()
uconfig = s_obj.config
sender_config = {
    "gsm_url" : uconfig["gsm_url"],
    "gsm_password" : uconfig["gsm_password"],
    "SMS_TIME_SLEEP" : uconfig["SMS_TIME_SLEEP"],
}

# В async проверять, какое время. Если время рассылать сообщения, то рассылаем сообщения
def check_send():
    """
    Метод, проверяющий какое сейчас время
    Когда время пришло, то заносит все данные с таблиц 1,2 в 3
    """

    while True:

        now_time = datetime.datetime.now()
        cur_hour = now_time.hour
        cur_minute = now_time.minute

        if cur_hour == uconfig["time_send"][0] and cur_minute == uconfig["time_send"][1]:

            #Обнуление таблицы №4 чтоб не присылалось вчерашнее расписание
            for k in r_id2timetable.keys():
                r_id2timetable.delete(k)


            obj = FATokenClass(uconfig)
            for number in r_number2group.keys():
                # Получаем данные с таблиц 1,2 в виде number и group_id
                group_name = r_number2group.get(number)
                group_id = r_group2id.get(group_name)

                #Если для этой группы еще нет расписания
                if r_id2timetable.exists(group_id)== False:

                    #Получаем расписание
                    time.sleep(uconfig["IOP_TIME_SLEEP"])
                    fa = fa_api_module.TTClass(obj.user_token, group_id, uconfig)

                    #Парсим расписание
                    obj = fa_json_module.JSONProcessingClass(group_name, fa.tt)
                    
                    #Пишем в Redis
                    r_id2timetable.set(group_id, obj.outstring)
                
                #Берем данные с Redis
                sms_content = r_id2timetable.get(group_id)
                if sms_content != "None":
                    #Добавляем в FIFO
                    queue.enqueue('sender.SendSMSClass', number, sms_content, sender_config)
            
            time.sleep(uconfig["ASYNC_PROC_TIME_SLEEP"])

        time.sleep(2)
