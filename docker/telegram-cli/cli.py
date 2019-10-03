"""
    Клиент Telegram для добавления данных абонентов
"""
import requests
import telegram
import time
import yaml
from telegram.error import NetworkError, Unauthorized

IP_ADDR = "127.0.0.1:5000"

class GetSettingsClass(object):
    """
    Класс для чтения настроек с yaml
    """
    def __init__(self):
        self.get_settings()
    
    def get_settings(self):
        with open("./settings.yml", 'r') as stream:
            self.c = yaml.safe_load(stream)

class TelegramCli(object):

    def __init__(self, token, admin_list):
        """Запуск бота"""
        self.update_id = None
        self.bot = telegram.Bot(token)
        self.admin_list = admin_list
        try:
            self.update_id = self.bot.get_updates()[0].update_id
        except IndexError:
            self.update_id = None

        while True:
            try:
                self.handler()
            except NetworkError:
                time.sleep(1)
            except Unauthorized:
                self.update_id += 1

    def check_admin(self, id):
        if int(id) in self.admin_list:
            return True
        return False

    def handler(self):
        p_mode = telegram.ParseMode.HTML
        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1
            
            tg_userid = str(update.message["chat"]["id"])

            if update.message.text == "/start":
                if self.check_admin(tg_userid) == True:
                    update.message.reply_text(
                        "Привет, ты авторизирован в системе с userid "+tg_userid+"\nДоступные команды:\n/add - добавление нового пользователя\n/remove - удаление пользователя",
                        parse_mode=p_mode)
                else:
                    update.message.reply_text(
                        "Нет доступа к админке!\n Для получния доступа обратись к методу /userid и отправь результат @Georgiy_D",
                        parse_mode=p_mode)

            elif update.message.text == "/userid":
                update.message.reply_text(
                    "Ваш userid в Telegram:\n<b>"+tg_userid+"</b>",
                    parse_mode=p_mode)
                
            elif update.message.text.split(" ")[0] == "/add" and self.check_admin(tg_userid) == True:
                
                args_list = update.message.text.split(" ")
                if len(args_list) != 3:
                    update.message.reply_text(
                        "Что-то пошло не так\nОбщий синтаксис команды:\n<b>/add номер_телефона группа</b>",
                        parse_mode=p_mode)
                
                else:
                    phone_number = args_list[1]
                    group = args_list[2]
                    update.message.reply_text(
                        "*Добавление номера телефона в систему*\nНомер телефона: <b>"+phone_number+"</b>\nГруппа: <b>"+group+"</b>",
                        parse_mode=p_mode)
                    r = requests.post("http://"+IP_ADDR+"/add_number", data={"number": phone_number, "group": group}).json()
                    if r["status"] == "ok":
                        update.message.reply_text("Успешное добавление пользователя")
                    elif r["exist"] == 1:
                        update.message.reply_text("Номер существует в БД, перезаписываем?")
                        if "ДА":
                            r.post()
                            update.message.reply_text("Успешное добавление пользователя")
                        else:
                            print("ПОФИГ")
                    else:
                        update.message.reply_text("Ошибка при добавлении пользователя!\nОписание: "+r["description"])
            
            elif update.message.text.split(" ")[0] == "/remove" and self.check_admin(tg_userid) == True:
                args_list = update.message.text.split(" ")
                if len(args_list) != 2:
                    update.message.reply_text(
                        "Что-то пошло не так\nОбщий синтаксис команды:\n<b>/remove номер_телефона</b>",
                        parse_mode=p_mode)
                else:
                    phone_number = args_list[1]
                    update.message.reply_text(
                        "*Удаление пользователя из системы*\nНомер телефона: <b>"+phone_number+"</b>",
                        parse_mode=p_mode)
                    r = requests.post("http://"+IP_ADDR+"/remove_number", data={"number": phone_number}).json()
                    if r["status"] == "ok":
                        update.message.reply_text("Успешное удаление пользователя")
                    else:
                        update.message.reply_text("Ошибка при удалении пользователя!\nОписание: "+r["description"])

def main():
    obj = GetSettingsClass()
    TelegramCli(obj.c["telegram_token"], obj.c["telegram_admins"])

if __name__ == '__main__':
    main()
