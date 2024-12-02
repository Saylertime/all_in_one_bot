from loader import bot
from utils.sheets import brief_is_free

@bot.message_handler(commands=['free_texts'])
def free_texts(message):
    free_authors = brief_is_free()
    if free_authors:
        messages = split_message_by_paragraphs(f"Сейчас свободны: \n\n{free_authors}")
        for msg in messages:
            bot.send_message(message.from_user.id, msg, parse_mode='Markdown', disable_web_page_preview=True)
            msg = f'Сейчас свободны: \n\n' \
                  f'{free_authors}'
    else:
        msg = 'Ого, всё раздали! Чмаффки <333!'

    bot.send_message(message.chat.id, msg, parse_mode='Markdown')


def split_message_by_paragraphs(message, max_length=4000):
    parts = []
    current_part = ""

    paragraphs = message.split("\n\n")

    for paragraph in paragraphs:
        if len(current_part) + len(paragraph) + 2 <= max_length:
            current_part += paragraph + "\n\n"
        else:
            parts.append(current_part.strip())
            current_part = paragraph + "\n\n"

    if current_part.strip():
        parts.append(current_part.strip())

    return parts
