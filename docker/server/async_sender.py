"""
Модуль для заполнения очереди FIFO в назначенное время
"""

import datetime
import time

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
            raise ValueError('Не могу авторизоваться в ИОП!')


r_number2group = redis.Redis(host='redis', port=6379, decode_responses=True, db=1)
r_group2id = redis.Redis(host='redis', port=6379, decode_responses=True, db=2)

# Подключение для создания очереди в Redis с помощью python-rq
queue = rq.Queue('sender-tasks', connection=redis.Redis.from_url('redis://redis:6379/3'))

s_obj = GetSettingsClass()
uconfig = s_obj.config

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

        #TODO ТУТ КАРОЧ С КОНФИГА БЕРЕМ ЗНАЧЕНИЯ
        if cur_hour == uconfig["time_send"][0] and cur_minute == uconfig["time_send"][1]:
            obj = FATokenClass(uconfig)
            keys = r_number2group.keys()
            for number in keys:
                # Получаем данные с таблиц 1,2 в виде number и group_id
                group_name = r_number2group.get(number)
                group_id = r_group2id.get(group_name)
                # Заносим в 3 таблицу
                queue.enqueue('sender.MainProcessingClass', number, group_id, group_name, obj.user_token, uconfig)
            time.sleep(uconfig["ASYNC_PROC_TIME_SLEEP"])

        time.sleep(2)
