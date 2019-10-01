"""
    Клиент Telegram для добавления данных абонентов
"""
import requests
import telegram
import time
import yaml
from telegram.error import NetworkError, Unauthorized

update_id = None



def main():
    """Запуск бота"""
    global update_id
    with open("./settings.yml", 'r') as stream:
        d = yaml.load(stream)
    token = d["telegram_token"]
    bot = telegram.Bot(token)
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            handler(bot)
        except NetworkError:
            time.sleep(1)
        except Unauthorized:
            update_id += 1


def handler(bot):
    global update_id
    p_mode = telegram.ParseMode.HTML
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1
        
        if update.message.text == "/start" : #AND ЕСТЬ В USER_ID ADMIN
            print(update.message)
            update.message.reply_text(
                "Привет 🐾\nЯ помогу тебе следить за конкурсом в списке предзачисления на сайте fa.ru\nДля активации введи команду вида\n<b>/set фамилия имя отчество</b>",
                parse_mode=p_mode)

        if update.message.text == "/userid":
            tg_userid = str(update.message["chat"]["id"])
            update.message.reply_text(
                "Ваш userid в Telegram:\n<b>"+tg_userid+"</b>",
                parse_mode=p_mode)
            
        elif update.message.text.split(" ")[0] == "/add":
            
            args_list = update.message.text.split(" ")
            args_list
            # Чтоб ФИО было полное
            if len(args_list) != 4:
                update.message.reply_text(
                    "Что-то пошло не так\nОбщий синтаксис команды:\n<b>/add номер_телефона группа</b>",
                    parse_mode=p_mode)
            
            else:
                 update.message.reply_text(
                    "Ты есть в списках, успешно добавил тебя в систему 😌\nТеперь ты будешь получать уведомления при изменении",
                    parse_mode=p_mode)


if __name__ == '__main__':
    main()
