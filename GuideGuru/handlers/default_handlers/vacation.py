from loader import bot
from psql_maker import author_on_vacation, update_vacation_status, find_author


admins = [68086662, 752393994]

@bot.message_handler(commands=['vacation'])
def vacation(message):
    username = "@" + message.from_user.username
    name_in_db = find_author(username)
    if name_in_db:
        vacation = author_on_vacation(message.from_user.username)[0]
        update_vacation_status(message.from_user.username, 'False' if vacation else 'True')
        bot.send_message(message.from_user.id, f'Теперь ты {"в отпуске" if not vacation else "снова работаешь"}!')
        msg = f"{name_in_db[0]} {'в отпуске' if not vacation else 'снова в строю'}"

        for admin in admins:
            bot.send_message(admin, msg)
    else:
        msg = f' {username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил'
        bot.send_message(message.from_user.id, msg, parse_mode='HTML')
