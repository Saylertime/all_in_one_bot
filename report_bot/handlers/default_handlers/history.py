from loader import bot
from states.overall import OverallState
from utils.sheets import rep_name_and_month

@bot.message_handler(commands=['history'])
def history(message):
    bot.send_message(message.chat.id, "Введи имя автора (как в таблице) и через запятую месяц и год. Пример:"
                                           "\n\nПаша, Январь 2024")
    bot.set_state(message.chat.id, state=OverallState.name)


@bot.message_handler(state=OverallState.name)
def answer(message):
    try:
        split_message = message.text.split(", ")
        name = split_message[0]
        current_month = split_message[1]
        msg = rep_name_and_month(name=name, month=current_month)
        bot.send_message(message.chat.id, msg, parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 'Введи нормально :(')
    finally:
        bot.delete_state(message.chat.id)
