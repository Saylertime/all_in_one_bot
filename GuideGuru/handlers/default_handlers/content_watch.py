from loader import bot
from utils.logger import logger
from utils.docs import get_content, check_text
from utils.content_watch import content_watch_check
from states.overall import OverallState
from psql_maker import find_author

@bot.message_handler(commands=['content_watch'])
def content_watch(message):
    logger.warning(f'{message.from_user.username} — команда CONTENT_WATCH')
    username = "@" + message.from_user.username
    name_in_db = find_author(username)
    if name_in_db:
        msg = ('Введи ссылку в формате \n\n'
               'https://docs.google.com/document/d/'
               '1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit')
        bot.set_state(message.from_user.id, state=OverallState.content_watch)
    else:
        msg = f'{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил'
    bot.send_message(message.from_user.id, msg)

@bot.message_handler(state=OverallState.content_watch)
def content_watch_answer(message):
    bot.delete_state(message.from_user.id)
    try:
        url = message.text.split('/')[5]
        full_text = get_content(url)
        msg = check_text(url) + '\n\n _____________________ \n\n'
        print('Достали контент')
        bot.send_message(message.from_user.id, 'Нужно подождать..... Если текст большой, проверка займёт пару минут')
        msg += str(content_watch_check(full_text))
        if len(msg) > 3999:
            bot.send_message(message.from_user.id,
                             'Очень много ссылок, откуда скопировано. Я не резиновый, чтобы все их вывести...')
        else:
            bot.send_message(message.from_user.id, msg)
    except Exception as error:
        bot.send_message(message.from_user.id, 'Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования')
        error = str(error) + f"\n\n{message.from_user.username}\n\n{message.text}"
        bot.send_message('68086662', error)
