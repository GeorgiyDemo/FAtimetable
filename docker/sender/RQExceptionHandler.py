"""
    Модуль обработки ошибок на уровне rq worker
    Вызывается, если было необработанное исключение в основной программе
"""
import redis

def writer(job, exc_type, exc_value, traceback):
    """
    Метод, вызываемый при ошибке в основной программе
    """

    #Говорим редиске, что у нас  +1 ошибка
    r_stats = redis.Redis(host='redis', port=6379, decode_responses=True, db=5)
    r_stats.incr("sms_errors")

    # Создаем JSON с данными об ошибке
    ExceptionResult = {
        "status": "exception",
        "description": str(exc_value),
    }
    print("Exception:",ExceptionResult)
    return False
