from loader import bot
from psql_maker import find_author
from utils.sheets import rep_name_and_month
from utils.calend import previous_month
from utils.logger import logger
import os

@bot.message_handler(commands=['history', 'last_month'])
def history(message, is_last_month=False):
    if message.text == '/last_month':
        is_last_month = True
    logger.warning(f'{message.from_user.username} — команда {"LAST_MONTH" if is_last_month else "HISTORY" }')
    username = "@" + message.from_user.username
    name_in_db = find_author(username)
    if name_in_db:
        if not is_last_month:
            msg = rep_name_and_month(name_in_db)
        else:
            msg = rep_name_and_month(name_in_db, previous_month())
            if os.path.isfile(msg):
                with open(msg, 'rb') as file:
                    bot.send_document(message.from_user.id, file)
    else:
        msg = f' {username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил'
    bot.send_message(message.from_user.id, msg, parse_mode='HTML')
