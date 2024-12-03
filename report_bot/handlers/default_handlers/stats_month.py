from loader import bot
from utils.sheets import stats_for_month
from utils.logger import logger
from states.overall import OverallState


@bot.message_handler(commands=['stats_month'])
def stats_month(message):
    logger.warning(f'{message.from_user.username} — команда stats_month')

    bot.send_message(message.chat.id, "Введи месяц с большой буквы и год через пробел. Пример:"
                                           "\n\nЯнварь 2024")
    bot.set_state(message.chat.id, state=OverallState.stats)


@bot.message_handler(state=OverallState.stats)
def answer(message):
    try:
        month = str(message.text)
        msg = stats_for_month(month)
        bot.send_message(message.chat.id, msg)
        bot.delete_state(message.from_user.id)
    except:
        bot.send_message(message.chat.id, 'Скорее всего, что-то не так ввели')