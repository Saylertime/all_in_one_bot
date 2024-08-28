from telebot.types import Message
from loader import bot
from pg_sql import all_users_from_db
from pg_maker_guide import new_table_stop_words, insert_new_word, delete_stop_word
from utils.logger import logger

@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """ Вызывается, когда пользователь без состояния вводит несуществующую команду """

    all_users, all_ids = all_users_from_db()

    if message.text == 'ВСЕ':
        all = ", ".join([i for i in all_users])
        bot.send_message(message.from_user.id, all)

    elif "ОПОВЕЩЕНИЕ: " in message.text:
        msg = " ".join(message.text.split()[1:])
        for id in all_ids:
            print(id)
            bot.send_message(id, msg)

    elif "ИСТОРИЯ" in message.text:
        with open('bot.log', 'r') as file:
            msg = "\n".join(file.readlines()[-20:])
            bot.send_message(message.from_user.id, f"{str(msg)}")

    elif "WORDS" in message.text:
        new_table_stop_words()
        bot.send_message(message.chat.id, 'Создана и обновлена')

    elif 'ДОБАВИТЬ' in message.text:
        word = str(message.text.split()[1])
        insert_new_word(word)
        bot.send_message(message.from_user.id, f'Слово "{word}" добавлено в базу запрещенных')


    elif 'УБРАТЬ' in message.text:
        word = str(message.text.split()[1])
        delete_stop_word(word)
        bot.send_message(message.from_user.id, f'Слово "{word}" удалено из базы запрещенных')


    else:
        logger.warning(f'{message.from_user.username} — ECHO — {message.text}')
        bot.reply_to(
            message, f"Такой команды нет: {message.text}\n"
                     f"Нажмите /start, чтобы посмотреть весь список команд"
        )

