"""
    Flask API
"""

import multiprocessing as mp

import async_sender
import redis
from flask import Flask, request
from flask_restful import Resource, Api

# Подключения к Redis для менеджмента данных
r_number2group = redis.Redis(host='redis', port=6379, decode_responses=True, db=1)
r_group2id = redis.Redis(host='redis', port=6379, decode_responses=True, db=2)
r_stats = redis.Redis(host='redis', port=6379, decode_responses=True, db=5)

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
        rewrite_flag = request.form.get('rewrite')
        if UtilClass.check_number(number) == False:
            return {"status": "exception", "description": "number is not valid", "exist" : 0}
        if UtilClass.check_group(group) == False:
            return {"status": "exception", "description": "group is not valid", "exist" : 0}
        try:
            if r_number2group.exists(number) == True and rewrite_flag == None:
                return {"status": "exception", "exist" : 1, "description": "Value already exist. POST field 'rewrite' with some value to rewrite the value"}
            else:
                r_number2group.set(number, group)
                return {"status": "ok", "exist": 0 }
        except:
            return {"status": "exception", "description": "can't set value to number2group table", "exist" : 0}


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
            r_group2id.set(group, group_id)
            return {"status": "ok"}
        except:
            return {"status": "exception", "description": "can't set value to group2id table"}

class Stats(Resource):
    def get(self):
        """
        Метод для получения статистики, ошибок,
        инфы и т д группы в БД
        """
        all_users = len(r_number2group.keys())
        all_sms = all_users*5

        redis_values_list = ["date_begin", "date_end", "sms_send", "sms_errors"]
        
        d = {
            "all_users" : str(all_users),
            "all_sms" : str(all_sms),
        }

        for k in redis_values_list:
            d[k] = r_stats.get(k)

        return d


api.add_resource(AddNumber, '/add_number')
api.add_resource(RemoveNumber, '/remove_number')
api.add_resource(AddGroup, '/add_group')
api.add_resource(Stats, '/stats')

if __name__ == '__main__':
    p = mp.Process(target=async_sender.check_send)
    p.start()
    app.run(host='0.0.0.0', debug=False)
