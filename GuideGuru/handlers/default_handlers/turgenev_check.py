from loader import bot
from utils.turgenev import check_text_in_turgenev
from utils.docs import get_content
from states.overall import OverallState
from psql_maker import find_author


@bot.message_handler(commands=['turgenev'])
def turgenev(message):
    username = "@" + message.from_user.username
    name_in_db = find_author(username)
    if name_in_db:
        msg = ("Введи ссылку в формате \n\n"
               "https://docs.google.com/document/d/1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit\n\n"
               "Критерии оценки: \n"
               "<b>До 5 баллов</b> — все хорошо\n"
               "<b>5-8 баллов</b> — средний риск\n"
               "<b>8-13</b> — нужно что-то делать\n"
               "<b>13+</b> – критическая ситуация.")
        bot.set_state(message.from_user.id, state=OverallState.turgenev)
    else:
        msg = f'{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил'
    bot.send_message(message.from_user.id, msg, parse_mode='HTML')

@bot.message_handler(state=OverallState.turgenev)
def turgenev_answer(message):
    bot.delete_state(message.from_user.id)
    try:
        url = message.text.split('/')[5]
        full_text = get_content(url)
        bot.send_message(message.from_user.id, 'Нужно подождать..... Если текст большой, проверка займёт пару минут')
        result = check_text_in_turgenev(full_text)
        bot.send_message(message.from_user.id, result, parse_mode='HTML')

    except Exception as error:
        bot.send_message(message.from_user.id, 'Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования')
        error = str(error) + f"\n\n{message.from_user.username}\n\n{message.text}"
        bot.send_message('68086662', error)
