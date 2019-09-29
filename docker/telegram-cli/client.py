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
    with open("./tokens.yaml", 'r') as stream:
        token = yaml.load(stream)
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
        
        if update.message.text == "/start":
            update.message.reply_text(
                "Привет 🐾\nЯ помогу тебе следить за конкурсом в списке предзачисления на сайте fa.ru\nДля активации введи команду вида\n<b>/set фамилия имя отчество</b>",
                parse_mode=p_mode)

        elif update.message.text.split(" ")[0] == "/set":
            name = update.message.text.split(" ")
            # Чтоб ФИО было полное
            if len(name) != 4:
                update.message.reply_text(
                    "Что-то пошло не так\nОбщий синтаксис команды:\n<b>/set фамилия имя отчество</b>",
                    parse_mode=p_mode)

                return 0
            name = name[1] + " " + name[2] + " " + name[3]
            update.message.reply_text("Ищем в списках \"" + name + "\" (может занять некоторое время)")
            r = requests.post("http://server:5000/adduser",
                              json={"tid": update.message.from_user.id, "username": name}).json()
            if r["status"] == "ok":
                update.message.reply_text(
                    "Ты есть в списках, успешно добавил тебя в систему 😌\nТеперь ты будешь получать уведомления при изменении",
                    parse_mode=p_mode)
            else:
                update.message.reply_text("Я не нашел тебя в списках 😔")


if __name__ == '__main__':
    main()
