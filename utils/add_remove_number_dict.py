import requests
import time

IP_ADDR = "157.245.54.111:5000"

meow = [
]

def add_number(number, group):
    print(number, group)
    print("[Добавление пользователя в систему]")
    r = requests.post("http://"+IP_ADDR+"/add_number", data={"number": number, "group": group})
    print(r.text)

for phone in meow:
    add_number(phone,"ПИ19-1")