from loader import bot
from pg_maker import all_authors
from utils.logger import logger

@bot.message_handler(commands=['authors'])
def authors(message):
    logger.warning(f'{message.from_user.username} — команда authors')
    msg = ''
    authors = all_authors()
    if authors:
        for author in authors:
            msg += f"{author[0]} — {author[1]}. В таблице: {author[2]}\n\n"
        print(authors)
    else:
        msg = 'Что-то с базой данных ;('
    bot.send_message(message.chat.id, msg)
