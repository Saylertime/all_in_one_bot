from loader import bot
from utils.sheets import brief_is_free
from utils.logger import logger

@bot.message_handler(commands=['free_texts'])
def free_texts(message):
    logger.warning(f'{message.from_user.username} — команда FREE_TEXTS')
    free_briefs = brief_is_free()
    if free_briefs:
        messages = split_message_by_paragraphs(f"Сейчас свободны: \n\n{free_briefs}")
        for msg in messages:
            bot.send_message(message.from_user.id, msg, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        msg = 'Ого, всё раздали! Чмаффки <333!'
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')


def split_message_by_paragraphs(message, max_length=4500):
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

    return list(dict.fromkeys(parts))