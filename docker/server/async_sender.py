"""
Модуль для заполнения очереди FIFO в назначенное время
"""
import rq
# Подключение для создания очереди в Redis с помощью python-rq
#queue = rq.Queue('opencv-tasks', connection=redis.Redis.from_url('redis://redis:6379/3'))

def async_template():
    #Получаем данные после Redis везде и потом закидываем в очередь FIFO
    #queue.enqueue('MainOpenCV.MainProcessingClass', pdf_base64, pdf_name, uuidstr, False, False, timeout=1000)
    pass
