from loader import bot
from pg_maker import find_for_tasks

def send_notifications():
    notifications = find_for_tasks()

    if notifications:
        for notification in notifications:
            user_id = notification[0]
            text = notification[2]
            bot.send_message(user_id, text, parse_mode='HTML')
