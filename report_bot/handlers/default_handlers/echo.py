from telebot.types import Message
from loader import bot
from pg_maker import refresh_db, delete_author, new_table, alter_db_add_vacation
from utils.text_ru import text_unique_check
from utils.sheets import rep_name_and_month_sber

@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """ Вызывается, когда пользователь без состояния вводит несуществующую команду """

    if message.text == 'ОБНОВИСЬ':
        refresh_db()
        bot.send_message(message.chat.id, 'Обновились')

    elif message.text == 'НАПОМИНАЛКА':
        new_table()
        bot.send_message(message.chat.id, 'Создана')

    elif "ALTER" in message.text:
        alter_db_add_vacation()
        bot.send_message(message.chat.id, 'Добавил...')

    elif "УДАЛИТЬ" in message.text:
        try:
            name = message.text.split(" ")[1]
            result = delete_author(name)
            if result:
                bot.send_message(message.chat.id, f"Мы будем скучать по тебе, {name} ;(")
            else:
                bot.send_message(message.chat.id, f"Такого нет. Может, мы его выперли уже давно?")
        except:
            bot.send_message(message.chat.id, f"Такого нет. Может, мы его выперли уже давно?")

    elif "TEXT" in message.text:
        left_symbs = text_unique_check()
        bot.send_message(message.chat.id, f"{left_symbs}")

    elif "SBER" in message.text or "СБЕР" in message.text:
        bot.send_message(message.from_user.id, str(rep_name_and_month_sber()))

    elif message.text == "сбер" or message.text == "sber":
        from utils.calendar import last_month
        bot.send_message(message.from_user.id, str(rep_name_and_month_sber(month=last_month())))


    elif "ИСТОРИЯ" in message.text:
        with open('bot.log', 'r') as file:
            msg = "\n".join(file.readlines()[-30:])
            bot.send_message(message.from_user.id, f"{str(msg)}")

    else:
        bot.reply_to(
            message, f"Такой команды нет: {message.text}\n"
                     f"Нажмите /start, чтобы посмотреть весь список команд"
        )
