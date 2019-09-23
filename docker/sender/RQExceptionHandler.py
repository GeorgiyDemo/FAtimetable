"""
    Модуль обработки ошибок на уровне rq worker
    Вызывается, если было необработанное исключение в основной программе
"""


def writer(job, exc_type, exc_value, traceback):
    """
    Метод, вызываемый при ошибке в основной программе
    """

    # Создаем JSON с данными об ошибке
    ExceptionResult = {
        "status": "exception",
        "description": str(exc_value),
    }
    print("ОШИБКА")
    print(ExceptionResult)
    return False
