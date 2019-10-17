import requests
IP_ADDR = "40.117.90.200:5000"

class MainClass(object):
    def __init__(self, flag, number, group):
        choose_dic = {
            1: self.add_number,
            2: self.delete_number,
        }

        self.number = number
        self.group = group
        choose_dic[flag]()

    def add_number(self):
        print("[Добавление пользователя в систему]")
        r = requests.post("http://"+IP_ADDR+"/add_number", data={"number": self.number, "group": self.group})
        print(r.text)

    def delete_number(self):
        print("[Удаление пользователя из системы]")
        r = requests.post("http://"+IP_ADDR+"/remove_number", data={"number": self.number})
        print(r.text)


def main():
    group = ""
    chooser = int(input("1. Добавление пользователя\n2. Удаление пользователя\n-> "))
    phone = input("Введите ваш номер телефона ->")
    if chooser == 1:
        group = input("Введите вашу группу -> ")
    MainClass(chooser, phone, group)


if __name__ == "__main__":
    main()
