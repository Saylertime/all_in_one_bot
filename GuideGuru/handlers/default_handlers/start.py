from loader import bot
from pg_sql import new_user
from keyboards.reply.create_markup import create_markup
from handlers.default_handlers.eldo import eldo
from handlers.default_handlers.mvideo import mvideo
from handlers.default_handlers.all_texts import all_texts
from handlers.default_handlers.check import check
from handlers.default_handlers.free_texts import free_texts
from handlers.default_handlers.history import history
from handlers.default_handlers.unique import unique
from utils.logger import logger


@bot.message_handler(commands=['start'])
def start_message(message):
    logger.warning(f'{message.from_user.username} — команда START')
    new_user(message.from_user.username, message.from_user.id)

    buttons = [('Правила оформления Эльдо', '1',),
               ('Правила оформления МВидео', '2'),
               ('Проверить текст на стоп-слова', '3'),
               ('Проверить текст на уникальность', '4'),
               ('Тексты за этот месяц', '5'),
               ('Тексты за прошлый месяц', '8'),
               ('Все твои тексты с ноября 2023', '6'),
               ('Свободные брифы', '7')]
    markup = create_markup(buttons)
    bot.send_message(message.from_user.id, "⬇⬇⬇ Ультимативный гайд для авторов GameGuru ⬇⬇⬇", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == '1':
        eldo(call)
    elif call.data == "2":
        mvideo(call)
    elif call.data == "3":
        check(call)
    elif call.data == "4":
        unique(call)
    elif call.data == "5":
        history(call, 'this')
    elif call.data == "6":
        all_texts(call)
    elif call.data == "7":
        free_texts(call)
    elif call.data == "8":
        history(call, 'last')
        # last_month(call)
    elif call.data == 'start':
        start_message(call)
