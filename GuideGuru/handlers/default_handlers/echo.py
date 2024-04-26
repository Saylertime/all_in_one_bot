from telebot.types import Message
from loader import bot
from pg_sql import all_users_from_db
from utils.logger import logger

@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """ Вызывается, когда пользователь без состояния вводит несуществующую команду """

    all_users, all_ids = all_users_from_db()

    if message.text == 'ВСЕ':
        all = ", ".join([i for i in all_users])
        bot.send_message(message.from_user.id, all)

    elif "ОПОВЕЩЕНИЕ: " in message.text:
        msg = " ".join(message.text.split()[1:])
        for id in all_ids:
            print(id)
            bot.send_message(id, msg)

    elif "ИСТОРИЯ" in message.text:
        with open('bot.log', 'r') as file:
            msg = "\n".join(file.readlines()[-20:])
            bot.send_message(message.from_user.id, f"{str(msg)}")


    else:
        logger.warning(f'{message.from_user.username} — ECHO — {message.text}')
        bot.reply_to(
            message, f"Такой команды нет: {message.text}\n"
                     f"Нажмите /start, чтобы посмотреть весь список команд"
        )

