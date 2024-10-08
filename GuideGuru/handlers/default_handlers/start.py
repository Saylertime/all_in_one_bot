from loader import bot
from pg_sql import new_user
from psql_maker import author_on_vacation
from keyboards.reply.create_markup import create_markup
from handlers.default_handlers.eldo import eldo
from handlers.default_handlers.mvideo import mvideo
from handlers.default_handlers.all_texts import all_texts
from handlers.default_handlers.check import check
from handlers.default_handlers.free_texts import free_texts
from handlers.default_handlers.history import history
from handlers.default_handlers.last_month import last_month
from handlers.default_handlers.unique import unique
from handlers.default_handlers.receipt import receipt
from handlers.default_handlers.vacation import vacation
from handlers.default_handlers.turgenev_check import turgenev
from utils.logger import logger


@bot.message_handler(commands=['start'])
def start_message(message):
    logger.warning(f'{message.from_user.username} — команда START')
    new_user(message.from_user.username, message.from_user.id)
    vacation = author_on_vacation(message.from_user.username)[0]

    buttons = [('Правила оформления Эльдо', '1',),
               ('Правила оформления МВидео', '2'),
               ('Проверить текст на стоп-слова', '3'),
               ('Проверить текст на уникальность', '4'),
               ('Проверить текст на в Turgenev', '10'),
               ('Загрузить чек', '9'),
               ('Тексты за этот месяц', '5'),
               ('Тексты за прошлый месяц', '8'),
               ('Все твои тексты с ноября 2023', '6'),
               ('Свободные брифы', '7'),
               (f'{"Хочу снова работать!!!" if vacation else "Иду в отпуск"}', 'vacation')]
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
        history(call)
    elif call.data == "6":
        all_texts(call)
    elif call.data == "7":
        free_texts(call)
    elif call.data == "8":
        last_month(call)
    elif call.data == "9":
        receipt(call)
    elif call.data == "10":
        turgenev(call)
    elif call.data == 'start':
        start_message(call)

    elif call.data == "vacation":
        vacation(call)
