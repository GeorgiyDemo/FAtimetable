"""
Модуль для заполнения очереди FIFO в назначенное время
"""

import datetime
import time

import fa_api_module
import fa_json_module
import sms_format_module

import redis
import requests
import rq
import yaml


class GetListSMSClass(object):

    """
    Метод для получения уникальных значений по индексу
    
    - Принимает глобальный list от sms_format_module
    - Отдаёт локальный list с уникальными значениями
    """

    def __init__(self, input_list):

        if input_list == "None":
            self.result = "None"
            self.updated_dict = "None"
        else:
            self.input_list = input_list
            self.getter()
            self.result = []
            self.updated_dict = {}

    def getter(self):
        sms_formater = self.input_list
        sms_list = []
        for key in sms_formater["sms_list"]:
            try:
                sms_index = sms_formater["sms_list"][key]["counter"]
                print(sms_index)
                print(sms_formater["sms_list"][key]["repeat_flag"])
                sms_element = sms_formater["sms_list"][key]["data"][sms_index]
            except:
                if sms_formater["sms_list"][key]["repeat_flag"] == True:
                    sms_formater["sms_list"][key]["counter"] = 0
                    sms_element = sms_formater["sms_list"][key]["data"][0]
                else:
                    raise IndexError("Вышли за пределы индекса, но флаг repeat_flag = False!")
        
            sms_formater["sms_list"][key]["counter"] += 1

            sms_list.append(sms_element)
            
        self.result = sms_list

        self.updated_dict = {
            "sms_list" : sms_formater["sms_list"],
        }

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

            #TODO Может сломаться случайно т.к. у токена ограниченное время действия
            fa_token = FATokenClass(uconfig)
            keys = r_number2group.keys()
            
            #TODO ТУТ МОЖНО СДЕЛАТЬ ОСНОВУ ДЛЯ СТАТИСТИКИ
            #Флаг для делея по кол-ву смс
            SMS_COUNTER = 0
            for number in keys:

                # Получаем данные с таблиц 1,2 в виде number и group_id
                group_name = r_number2group.get(number)
                group_id = r_group2id.get(group_name)

                #Если для этой группы еще нет расписания
                if r_id2timetable.exists(group_id) == False:

                    #Получаем расписание
                    time.sleep(uconfig["IOP_TIME_SLEEP"])
                    fa = fa_api_module.TTClass(fa_token.user_token, group_id, uconfig)
                    #Парсим расписание
                    obj = fa_json_module.JSONProcessingClass(group_name, fa.tt)

                    #Все возможные комбинации сообщений
                    sms_formater = sms_format_module.SMSFormaterClass(obj.outstring)
                    
                    #Пишем в Redis
                    r_id2timetable.set(group_id, sms_formater.outd)
                    
                    #Получаем уникальные sms
                    sms_list_obj = GetListSMSClass(sms_formater.outd)

                    #Пишем в Redis обновлённый индекс
                    r_id2timetable.set(group_id, sms_list_obj.updated_dict)
                    
                    sms_content = sms_list_obj.result
                
                else:
                    
                    #Берем данные с Redis
                    outd = r_id2timetable.get(group_id)
                    #Получаем уникальные sms
                    sms_list_obj = GetListSMSClass(outd)

                    #Пишем в Redis обновлённый индекс
                    r_id2timetable.set(group_id, sms_list_obj.updated_dict)
                    
                    sms_content = sms_list_obj.result

                
                if sms_content != "None":
                    #Добавляем в FIFO
                    queue.enqueue('sender.SendSMSClass', number, sms_content, sender_config)
                    SMS_COUNTER += 1
                
                if SMS_COUNTER == 6:
                    time.sleep(uconfig["30SMS_TIME_LIMIT"])
                    SMS_COUNTER = 0


        time.sleep(2)
