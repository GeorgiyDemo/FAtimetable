"""
    Flask API для 
"""

import async_sender

import base64
import os
import redis
import multiprocessing as mp
from flask import Flask, request
from flask_restful import Resource, Api

# Подключения к Redis для менеджмента данных
r_number2group = redis.Redis(host='redis', port=6379, decode_responses=True, db=1)
r_group2id = redis.Redis(host='redis', port=6379, decode_responses=True, db=2)

app = Flask(__name__)
api = Api(app)

class UtilClass(object):
    @staticmethod
    def check_number(n):
        if n.startswith("+7") and len(n) == 12:
            return True
        return False

    @staticmethod
    def check_group(g):
        if r_group2id.exists(g) == True:
            return True
        return False

class AddNumber(Resource):
    def post(self):
        """
        Метод для добавления номера телефона в БД
        
        - Получает номер телефона number
        - Получает группу group
        """ 
        number = request.form.get('number')
        group = request.form.get('group')
        if UtilClass.check_number(number) == False:
            return {"status": "exception", "description": "number is not valid"}
        if UtilClass.check_group(group) == False:
            return {"status": "exception", "description": "group is not valid"}
        try:
            r_number2group.set(number, group)
            return {"status": "ok"}
        except:
            return {"status": "exception", "description": "can't set value to number2group table"}

class RemoveNumber(Resource):
    def post(self):
        """
        Метод для удаления номера телефона в БД
        
        - Получает номер телефона number
        """ 
        number = request.form.get('number', '')
        if UtilClass.check_number(number) == False:
            return {"status": "exception", "description": "number is not valid"}
        if r_number2group.exists(number) == False:
            return {"status": "exception", "description": "number not exists"}
        r_number2group.delete(number)
        return {"status": "ok"}

class AddGroup(Resource):
    def post(self):
        """
        Метод для добавления группы в БД
        
        - Получает имя группы group
        - Получает id группы
        - Заносит ассоциацию в БД
        """ 
        group = request.form.get('group', '')
        group_id = request.form.get('id', '')
        try:
            r_group2id.set(group,group_id)
            return {"status": "ok"}
        except:
            return {"status": "exception", "description": "can't set value to group2id table"}

#TODO Статистика/статус сервисов и т.д.
class Stats(Resource):
    def get(self):
        """
        Метод для получения статистики, ошибок,
        инфы и т д группы в БД
        """ 
        return {"status": "ok","containers":"VSYO NORMALNO"}

api.add_resource(AddNumber, '/add_number')
api.add_resource(RemoveNumber, '/remove_number')
api.add_resource(AddGroup, '/add_group')
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    p = mp.Process(target=async_sender.check_send)
    p.start()
    app.run(host='0.0.0.0', debug=False)