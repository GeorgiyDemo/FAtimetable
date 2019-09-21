import requests

class MainClass(object):
    def __init__(self, number, group):
        self.number = number
        self.group = group
        self.add_number()
        #self.delete_number()
    
    def add_number(self):
        r = requests.get("http://127.0.0.1:5000/add_number?number="+self.number+"&group="+self.group)
        print(r.text)
    
    def delete_number(self):
        r = requests.post("http://127.0.0.1:5000/remove_number?number="+self.number)
        print(r.text)

def main():
    group = input("Введите вашу группу -> ")
    phone = input("Введите ваш номер телефона ->")
    MainClass(phone, group)


if __name__ == "__main__":
    main()