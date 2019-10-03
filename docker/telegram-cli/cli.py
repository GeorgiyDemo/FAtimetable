"""
    Клиент Telegram для добавления данных абонентов
"""
import requests
import telegram
import time
import yaml
from telegram.error import NetworkError, Unauthorized

IP_ADDR = "server:5000"

class GetSettingsClass(object):
    """
    Класс для чтения настроек с yaml
    """
    def __init__(self):
        self.get_settings()
    
    def get_settings(self):
        with open("./yaml/settings.yml", 'r') as stream:
            self.c = yaml.safe_load(stream)

class TelegramCli(object):

    def __init__(self, token, admin_list):
        
        """
        Запуск бота
        """
        
        self.d_flag = {}
        self.d_data = {}

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
                        "Привет, ты авторизован в системе с userid "+tg_userid+"\nДоступные команды:\n/add - добавление нового пользователя\n/remove - удаление пользователя",
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

                        keyboard = [
                            ['Да', 'Нет'], 
                        ]
                        self.d_flag[tg_userid] = -1
                        self.d_data[tg_userid] = {"number" : phone_number, "group" : group}
                        reply_markup = telegram.ReplyKeyboardMarkup(keyboard)
                        self.bot.send_message(chat_id=tg_userid, 
                                        text="Номер существует в БД, перезаписываем?", 
                                        reply_markup=reply_markup)

                    else:
                        update.message.reply_text("Ошибка при добавлении пользователя!\nОписание: "+r["description"])
            
            elif (update.message.text == "Да") and (tg_userid in self.d_flag) and (self.d_flag[tg_userid] == -1):
                
                input_number = self.d_data[tg_userid]["number"]
                input_group = self.d_data[tg_userid]["group"]
                data = {
                    "number": input_number, 
                    "group": input_group, 
                    "rewrite": True,
                }
                r = requests.post("http://"+IP_ADDR+"/add_number",data=data).json()
                del self.d_data[tg_userid]
                self.d_flag[tg_userid] = 1
                reply_markup = telegram.ReplyKeyboardRemove()
                if r["status"] == "ok":
                    self.bot.send_message(chat_id=tg_userid, text="Успешная перезапись пользователя "+input_number+" в группу "+input_group,
                    reply_markup=reply_markup)
                else:
                    self.bot.send_message(chat_id=tg_userid, text="Что-то совсем всё плохо\nПиши @Georgiy_D и рассказывай как ты дошёл до такой жизни",
                    reply_markup=reply_markup)

            elif (update.message.text == "Нет") and (tg_userid in self.d_flag) and (self.d_flag[tg_userid] == -1):
                del self.d_data[tg_userid]
                reply_markup = telegram.ReplyKeyboardRemove()
                self.bot.send_message(chat_id=tg_userid, text="На нет и суда нет, хих", reply_markup=reply_markup)
                self.d_flag[tg_userid] = 0

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
