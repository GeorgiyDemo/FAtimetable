"""
Модуль для заполнения очереди FIFO в назначенное время
"""
import time
import datetime
import rq
import redis
import yaml
import requests

class FATokenClass(object):
    """
    Класс для получения токена и id пользователя ИОП 

    - Авторизуется с логином/паролем в settings.yaml
    - В self.user_data отдаёт tuple с токеном и id пользователя
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }
        self.get_settings()
        self.get_token_site()

    def get_settings(self):
        with open("./settings.yml", 'r') as stream:
            self.config = yaml.safe_load(stream)

    def get_token_site(self):
        session = requests.session()
        session.cookies['ASP.NET_SessionId'] = self.get_cookies_site()
        #Устанавливаем сессию requests с токеном
        self.user_token = session
    
    def get_cookies_site(self):
        """
        Получение cookies по логину и паролю на сайте ИОП
        """
        session = requests.session()
        response = session.post('https://portal.fa.ru/CoreAccount/LogOn',
            data={'Login': self.config["login"], 'Pwd': self.config["password"]},
            headers=self.headers,allow_redirects=True)
        data = session.cookies['ASP.NET_SessionId']
        session.close()
        if response.url == 'https://portal.fa.ru/CoreAccount/Portal':
            return data
        else:
            raise ValueError('Не могу авторизоваться!')

r_number2group = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, db=1) #host = redis
r_group2id = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, db=2) #host = redis

# Подключение для создания очереди в Redis с помощью python-rq
queue = rq.Queue('sender-tasks', connection=redis.Redis.from_url('redis://127.0.0.1:6379/3')) #127.0.0.1 -> redis
obj = FATokenClass()


#В async проверять, какое время. Если время рассылать сообщения, то рассылаем сообщения
def check_send():
    """
    Метод, проверяющий какое сейчас время
    Когда время пришло (#TODO) заносит все данные с таблиц 1,2 в 3
    """
    SEND_FLAG = False
    while True:
        
        now_time = datetime.datetime.now()
        cur_hour = now_time.hour
        cur_minute = now_time.minute

        if cur_hour == 0 and cur_minute == 0:
            SEND_FLAG = False

        if cur_hour == 13 and cur_minute == 9 and SEND_FLAG == False:
            print("ОГО РАССЫЛКА НАЧАЛАСЬ")
            keys = r_number2group.keys()
            for number in keys:
                #Получаем данные с таблиц 1,2 в виде number и group_id
                group_name = r_number2group.get(number)
                group_id = r_group2id.get(group_name)
                #Заносим в 3 таблицу
                queue.enqueue('sender.MainProcessingClass', number, group_id, group_name, obj.user_token)
            SEND_FLAG == True

        time.sleep(2)