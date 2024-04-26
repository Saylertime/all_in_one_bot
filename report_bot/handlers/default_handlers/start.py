from loader import bot

@bot.message_handler(commands=['start'])
def start_message(message):

    msg = f"Ультимативный бот для сотрудников ГейГуру \n\n" \
          f"/free_authors — Свободные авторы \n\n" \
          f"/free_texts — Свободные брифы \n\n" \
          f"/deadlines — Дедлайны \n\n" \
          f"/notification — Напоминалка \n\n" \
          f"/history — Инфа по автору за выбранный месяц \n\n" \
          f"/all_texts — Все тексты автора за всё время \n\n" \
          f"/new_author — Добавить нового автора \n\n" \
          f"/authors — Все авторы \n\n" \
          f"/money — Гонорары за месяц\n\n"\
          f"/stats_month — Статистика за месяц\n\n"

    bot.send_message(message.chat.id, msg)
