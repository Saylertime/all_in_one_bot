from loader import bot
from utils.receipt_sheets import get_data_from_sheet, new_list
from states.overall import CheckState
from psql_maker import find_author
import re


@bot.message_handler(commands=['receipt'])
def receipt(message):
    username = "@" + message.from_user.username
    name_in_db = find_author(username)
    if name_in_db:
        msg = f"Закинь сюда ссылку на чек. Больше ничего не надо — ни имени, ни месяца"
        bot.send_message(message.from_user.id, msg)
        bot.set_state(message.from_user.id, state=CheckState.check)
    else:
        bot.send_message(message.from_user.id, 'Тебя нет в базе данных... Обратись к @saylertime, чтобы он порешал')


@bot.message_handler(state=CheckState.check)
def upload_link(message):
    bot.delete_state(message.from_user.id)
    if contains_ru_domain(message.text):
        full_name = get_data_from_sheet(message.from_user.username)
        new_list(full_name, message.text)
        bot.send_message(message.from_user.id, 'Спасибо, всё получилось')
    else:
        bot.send_message(message.from_user.id, 'Это точно ссылка? Не вижу в ней .ru. Начни всё заново')


def contains_ru_domain(url):
    ru_pattern = re.compile(r'\.ru\b', re.IGNORECASE)
    return re.search(ru_pattern, url) is not None