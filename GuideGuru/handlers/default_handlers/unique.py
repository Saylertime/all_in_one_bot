from loader import bot
from utils.logger import logger
from utils.docs import get_content
from utils.text_ru import text_unique_check, symbols_left
from states.overall import OverallState


@bot.message_handler(commands=['unique'])
def unique(message):
    logger.warning(f'{message.from_user.username} — команда UNIQUE')
    bot.send_message(message.from_user.id, 'Введи ссылку в формате \n\n'
                                      'https://docs.google.com/document/d/'
                                      '1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit')
    bot.set_state(message.from_user.id, state=OverallState.unique)

@bot.message_handler(state=OverallState.unique)
def unique_answer(message):
    try:
        url = message.text.split('/')[-2]
        full_text = get_content(url)
        print('Достали контент')
        symb = int(symbols_left().replace(",", ""))
        if not len(full_text) > symb:
            bot.send_message(message.from_user.id, 'Нужно подождать..... Если текст большой, проверка займёт пару минут')
            msg = text_unique_check(full_text)
            if len(msg) > 3999:
                bot.send_message(message.from_user.id,
                                 'Очень много ссылок, откуда скопировано. Я не резиновый, чтобы все их вывести...')
            else:
                bot.send_message(message.from_user.id, msg)
    except Exception as error:
        bot.send_message(message.from_user.id, 'Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования')
        error = str(error) + f"\n\n{message.from_user.username}\n\n{message.text}"
        bot.send_message('68086662', error)
    finally:
        bot.delete_state(message.from_user.id)
