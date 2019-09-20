import redis

r = redis.Redis(host='127.0.0.1', port=6379, db=1)
# задаем параметры базы redis: находится на localhost, стандартный порт 6379, номер базы 1 (по дефолту создается сразу 16: от 0 до 15)
# добавляем модуль redis

# присваиваем переменной test1 значение 5
r.set('test1', "mewowww")
meow = r.get("test1").decode("utf-8")
print(meow+"1")
print(r.exists("av"))
print(r.exists("test1"))
