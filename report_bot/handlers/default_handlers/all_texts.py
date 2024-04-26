from loader import bot
from states.overall import OverallState
from utils.sheets import all_texts_of_author


@bot.message_handler(commands=['all_texts'])
def all_texts(message):
    bot.send_message(message.chat.id, "Введи имя автора (как в таблице) Пример:"
                                      "\n\nПаша")
    bot.set_state(message.chat.id, state=OverallState.all_texts)


@bot.message_handler(state=OverallState.all_texts)
def answer(message):
    all_texts_eldo, all_texts_mvideo = all_texts_of_author(message.text)
    if all_texts_eldo:
        with open(all_texts_eldo, 'rb') as file:
            bot.send_document(message.chat.id, file)
    if all_texts_mvideo:
        with open(all_texts_mvideo, 'rb') as file:
            bot.send_document(message.chat.id, file)
    if not all_texts_eldo and not all_texts_mvideo:
        msg = "Ничего не нашел по нему( Точно имя правильное?"
        bot.send_message(message.chat.id, msg)
    bot.delete_state(message.chat.id)
