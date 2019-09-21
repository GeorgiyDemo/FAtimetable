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

# Подключение для получения результатов обработки документов
r_number2group = redis.Redis(host='127.0.0.1', port=6379, db=1) #host = redis
r_group2id = redis.Redis(host='127.0.0.1', port=6379, db=2) #host = redis

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
    def get(self):
        """
        Метод для добавления номера телефона в БД
        
        - Получает номер телефона number
        - Получает группу group
        """ 
        number = request.args.get('number', '')
        group = request.args.get('group', '')
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
    def get(self):
        """
        Метод для удаления номера телефона в БД
        
        - Получает номер телефона number
        """ 
        number = request.args.get('number', '')
        if UtilClass.check_number(number) == False:
            return {"status": "exception", "description": "number is not valid"}
        if r_number2group.exists(number) == False:
            return {"status": "exception", "description": "number not exists"}
        r_number2group.delete(number)
        return {"status": "ok"}

class AddGroup(Resource):
    def get(self):
        """
        Метод для добавления группы в БД
        
        - Получает имя группы group
        - Получает id группы
        - Заносит ассоциацию в БД
        """ 
        group = request.args.get('group', '')
        group_id = request.args.get('id', '')
        try:
            r_group2id.set(group,group_id)
            return {"status": "ok"}
        except:
            return {"status": "exception", "description": "can't set value to group2id table"}


api.add_resource(AddNumber, '/add_number')
api.add_resource(RemoveNumber, '/remove_number')
api.add_resource(AddGroup, '/add_group')

if __name__ == '__main__':
    i = 2
    p = mp.Process(target=async_sender.main, args=(i,))
    p.start()
    app.run(host='127.0.0.1', debug=False)
    #app.run(host='0.0.0.0', debug=False)