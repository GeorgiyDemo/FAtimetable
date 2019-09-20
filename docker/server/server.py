"""
    Flask API для 
"""

import base64
import json
import os
import redis
from flask import Flask, request
from flask_restful import Resource, Api

# Подключение для получения результатов обработки документов
r_number2group = redis.Redis(host='127.0.0.1', port=6379, db=1) #host = redis
r_group2id = redis.Redis(host='127.0.0.1', port=6379, db=2) #host = redis

app = Flask(__name__)
api = Api(app)

#Скорее всего во внешний модуль выкинуть ващ
#В async проверять, какое время. Если время рассылать сообщения, то рассылаем сообщения

class AddNumber(Resource):
    def get(self):
        """
        Метод для добавления номера телефона в БД
        
        - Получает номер телефона number
        - Получает группу group
        """ 
        
        number = request.args.get('number', '')
        group = request.args.get('group', '')
        return {number: group}

class RemoveNumber(Resource):
    def get(self):
        """
        Метод для удаления номера телефона в БД
        
        - Получает номер телефона number
        """ 
        number = request.args.get('number', '')
        return {"MEOW"}
        #Работа с FIFO
        #Работа с Redis
        #r.set(uuidstr, json.dumps({"status": "in pool"}))
        #return json.dumps({"status": "exception", "description": "file is not a .pdf file"})

api.add_resource(AddNumber, '/add_number')
api.add_resource(RemoveNumber, '/remove_number')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
    #app.run(host='0.0.0.0', debug=False)