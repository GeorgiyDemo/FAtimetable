"""
    Модуль обработки ошибок на уровне rq worker
    Вызывается, если было необработанное исключение в основной программе
"""
import json
import pymysql.cursors
import redis
import requests
import yaml
from sentry_sdk import init


def check_internet():
    url = 'http://www.google.com/'
    timeout = 5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def ExceptionWriter(job, exc_type, exc_value, traceback):
    """
    Метод, вызываемый при ошибке в основной программе
    """

    # Создаем JSON с данными об ошибке
    ExceptionResult = {
        "status": "exception",
        "pages": [{"qc": 3, "exception": str(exc_value)}]
    }

    # Записываем данные об ошибке в Redis
    redis_connect = redis.Redis(host='redis', port=6379, db=1)
    redis_connect.set(job.args[2], json.dumps(ExceptionResult))

    # Если есть флаг записи в MySQL от клиента
    if job.args[3] == True:

        # данные о соединении БД
        with open("./yaml/DBlist.yaml", 'r') as stream:
            DBLogin = yaml.load(stream)

        connection = pymysql.connect(host=DBLogin[0], port=DBLogin[1], user=DBLogin[2], password=DBLogin[3],
                                     db=DBLogin[4], cursorclass=pymysql.cursors.DictCursor, autocommit=False)
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE tasks SET status ='exception', result =%s WHERE job_id='" + job.args[2] + "';",
                           json.dumps(ExceptionResult))
        except:
            connection.rollback()
            connection.close()
            raise
        else:
            connection.commit()
            connection.close()

    # Соединение с sentry.io и передача Exception
    if check_internet() == True:
        with open("./yaml/SentryIOURL.yaml", 'r') as stream:
            SentryConnection = yaml.load(stream)
        init(SentryConnection)
        raise Exception

    return False
