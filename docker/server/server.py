"""
    Flask API для 
"""

import base64
import json
import os
import redis
import rq
from flask import Flask, request

#В async проверять, какое время. Если время рассылать сообщения, то рассылаем сообщения
def async_template():
    #Получаем данные после Redis везде и потом закидываем в очередь FIFO
    queue.enqueue('MainOpenCV.MainProcessingClass', pdf_base64, pdf_name, uuidstr, False, False, timeout=1000)



app = Flask(__name__)
# Подключение для получения результатов обработки документов
r = redis.Redis(host='redis', port=6379, db=1)
# Подключение для создания очереди в Redis с помощью python-rq
queue = rq.Queue('opencv-tasks', connection=redis.Redis.from_url('redis://redis:6379/0'))

#TODO переделать на POST
@app.route('/add_number', methods=['GET'])
def add_number():
    """
    Метод для добавления номера телефона в БД
    
    - Получает номер телефона number
    - Получает группу group
    """ 
    
    number = request.args.get('number', '')
    group = request.args.get('group', '')


@app.route('/remove_number', methods=['GET'])
def remove_number():
    """
    Метод для удаления номера телефона в БД
    
    - Получает номер телефона number
    """ 
    number = request.args.get('number', '')
    #Работа с FIFO
    queue.enqueue('MainOpenCV.MainProcessingClass', pdf_base64, pdf_name, uuidstr, False, False, timeout=1000)
    #Работа с Redis
    r.set(uuidstr, json.dumps({"status": "in pool"}))
    return json.dumps({"status": "exception", "description": "file is not a .pdf file"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
