"""
Пример работы с модулем fa_api
"""
import fa_api
import datetime

def get_date_tomorrow():
    
    """
    Метод для получения завтрашнего дня
    """

    today = datetime.date.today()
    future = today + datetime.timedelta(days=1)
    return future.strftime("%d.%m.%Y")


def main():

    #Создаём объект
    fa = fa_api.FaClass()

    #Обращаемся к методу get_group
    group = fa.get_group()
    print(group)

    #Получаем расписание на завтра
    tt = fa.get_timetable_byday(get_date_tomorrow())
    print(tt)

if __name__ == "__main__":
    main()