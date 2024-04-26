from loader import bot
from states.overall import OverallState
from pg_maker import add_author, refresh_db


@bot.message_handler(commands=['new_author'])
def new_author(message):
#     refresh_db()
#     bot.send_message(message.chat.id, "Обновились")

    bot.send_message(message.from_user.id, "Введи имя и фамилию автора, ник и то, как помечаем его в таблице. "
                                           "Всё через запятую с пробелом. Пример: \n\n"
                                           "Паша Ручкин, @pekron, Паша")
    bot.set_state(message.from_user.id, OverallState.new_author)

@bot.message_handler(state=OverallState.new_author)
def add_author_to_db(message):
    try:
        name, nickname, name_in_db = message.text.split(', ')
        add_author(name, nickname, name_in_db)
        bot.send_message(message.from_user.id, f"{nickname} добавлен!\n\n"
                                               f"Добавить еще одного — /new_author\n\n"
                                               f"Посмотреть всех — /authors")
    except:
        pass
        bot.send_message(message.from_user.id, f"Что-то не получилось. \n"
                                               f"Попробовать еще раз — /new_author\n"
                                               f"Посмотреть всех — /authors")
    finally:
        bot.delete_state(message.chat.id)

