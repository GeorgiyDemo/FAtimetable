"""
Модуль для заполнения очереди FIFO в назначенное время
"""
import time
import datetime
import rq
import redis

r_number2group = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, db=1) #host = redis
r_group2id = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True, db=2) #host = redis

# Подключение для создания очереди в Redis с помощью python-rq
queue = rq.Queue('sender-tasks', connection=redis.Redis.from_url('redis://127.0.0.1:6379/3')) #redis

#В async проверять, какое время. Если время рассылать сообщения, то рассылаем сообщения
def check_send():
    """
    Метод, проверяющий какое сейчас время
    Когда время пришло (#TODO) заносит все данные с таблиц 1,2 в 3
    """
    while True:
        now_time = datetime.datetime.now()
        cur_hour = now_time.hour
        cur_minute = now_time.minute

        if cur_hour == 6 and cur_minute == 40:
            keys = r_number2group.keys()
            print(keys)
            for number in keys:
                #Получаем данные с таблиц 1,2 в виде number и group_id
                group_id = r_group2id.get(r_number2group.get(number))
                #Заносим в 3 таблицу
                queue.enqueue('sender.MainProcessingClass', number, group_id)
