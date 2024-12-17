from loader import bot
from utils.docs import get_content_with_links
from states.overall import OverallState
from utils.logger import logger
import re


@bot.message_handler(commands=['get_ids'])
def get_ids(message):
    logger.warning(f'{message.from_user.username} — команда GET_IDS')
    bot.send_message(message.from_user.id, 'Кидай ссылку на документ, из которого надо достать ID.\n\n'
                                      'Ссылка должна выглядеть так.\n\n'
                                      'https://docs.google.com/document/d/136QHaIF8G_w6fJzTJIstoA0sKRwNElsTAzzXyJ0xwj8/edit')
    bot.set_state(message.from_user.id, state=OverallState.get_ids)


@bot.message_handler(state=OverallState.get_ids)
def get_ids_answer(message):
    try:
        url = message.text.split('/')[-2]
        links = get_content_with_links(url)
        if links:
            bot.send_message(message.from_user.id, str("ID товаров: " + get_product_ids(links)))
    except:
        bot.send_message(message.from_user.id, 'Похоже, ссылкая кривая, не тот формат или доступ для редактирования закрыт')
    finally:
        bot.delete_state(message.from_user.id)


def get_product_ids(content):
    pattern = r'https://www\.mvideo\.ru/products/[a-zA-Z0-9\-\_]+-\d+'
    links = [link for link in content if re.match(pattern, link)]
    if links:
        ids = set([link.split('-')[-1] for link in links])
        return ', '.join(ids)
    return 'Кажется, ссылок в тексте нет'
