from loader import bot
from states.overall import OverallState
from pg_maker import new_table, new_notifications, find_notifications, drop_table, find_for_tasks

@bot.message_handler(commands=['notification'])
def notification(message):
    new_table()
    msg = 'Введи дату, время и текст напоминалки через пробел. Пример:\n\n29.03 15:33 Вычитать текст Фила про депрессию'
    bot.send_message(message.chat.id, msg)
    bot.set_state(message.chat.id, OverallState.notifications)

@bot.message_handler(state=OverallState.notifications)
def save_notification(message):
    try:
        message_parts = message.text.split(" ", 2)
        n_date = message_parts[0]
        n_time = message_parts[1]
        text = message_parts[2]
        new_notifications(user_id=message.from_user.id, n_date=n_date, n_time=n_time, text=text)
        bot.send_message(message.from_user.id, f'Уведомление придет {n_date} в {n_time}')
        bot.delete_state(message.from_user.id)
    except:
        bot.send_message(message.from_user.id, 'Что-то пошло не так. Попробуй еще раз')
