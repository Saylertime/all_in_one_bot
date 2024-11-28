from loader import bot
from utils.sheets import who_is_free
from pg_maker import authors_on_vacation

@bot.message_handler(commands=['free_authors'])
def free_authors(message):
    free_authors, authors_with_text, authors_with_few_texts = who_is_free()
    on_vacation = authors_on_vacation()

    if free_authors:
        msg = 'Сейчас свободны: \n\n'
        for author in free_authors:
            msg += f"{author[1]} — {author[0]}\n"

        msg +='\nАвторы с одним текстом: \n\n'
        for author in authors_with_text:
            msg += f"{author[1]} — {author[0]}\n"

        msg += '\nОчень занятые авторы: \n\n'
        for author in authors_with_few_texts:
            msg += f"{author[1]} — {author[0]}\n"

        if on_vacation:
            msg += '\nАвторы в отпуске: \n\n'
            for author in on_vacation:
                msg += f"{author[2]} — {author[1]}\n"
        bot.send_message(message.chat.id, msg)

    else:
        bot.send_message(message.chat.id, 'Все такие занятые, я прям не могу(((')



