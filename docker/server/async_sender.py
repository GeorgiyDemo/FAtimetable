"""
Модуль для заполнения очереди FIFO в назначенное время
"""
import time
import rq
import redis
# Подключение для создания очереди в Redis с помощью python-rq
queue = rq.Queue('sender-tasks', connection=redis.Redis.from_url('redis://redis:6379/3'))

#В async проверять, какое время. Если время рассылать сообщения, то рассылаем сообщения
def main(i):
    while True:
        print(i)
        time.sleep(10)
        i += 1
    #Получаем данные после Redis везде и потом закидываем в очередь FIFO
    queue.enqueue('sender.MainProcessingClass', number, group_id, timeout=1000)
    pass
