from loader import bot
from utils.sheets import brief_is_free

@bot.message_handler(commands=['free_texts'])
def free_texts(message):
    free_authors = brief_is_free()
    if free_authors:
        msg = f'Сейчас свободны: \n\n' \
              f'{free_authors}'
    else:
        msg = 'Ого, всё раздали! Чмаффки <333!'

    bot.send_message(message.chat.id, msg, parse_mode='Markdown')
