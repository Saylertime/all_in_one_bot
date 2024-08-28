from loader import bot
from psql_maker import find_author
from utils.sheets import rep_name_and_month, rep_name_and_month_sber
from utils.logger import logger
import os

@bot.message_handler(commands=['history'])
def history(message):
    logger.warning(f'{message.from_user.username} — команда {"HISTORY" }')
    username = "@" + message.from_user.username
    name_in_db = find_author(username)
    if name_in_db:
        sber_data = rep_name_and_month_sber(name_in_db)
        if sber_data:
            msg = rep_name_and_month(name_in_db, sber_data=sber_data)
            if os.path.isfile(msg):
                with open(msg, 'rb') as file:
                    bot.send_document(message.from_user.id, file)
    else:
        msg = f' {username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил'
    bot.send_message(message.from_user.id, msg, parse_mode='HTML')

    # bot.send_message(message.from_user.id, rep_name_and_month_sber(name_in_db),  parse_mode='HTML')

