from psql_maker import author_on_vacation
from keyboards.reply.create_markup import create_markup


from aiogram import Router
from aiogram.filters import CommandStart

router_start = Router()


@router_start.message(CommandStart())
async def start_message(message):
    vacation = await author_on_vacation(message.from_user.username)

    buttons = [('Правила оформления Эльдо', 'eldo',),
               ('Правила оформления МВидео', 'mvideo'),
               ('Проверить текст на стоп-слова', 'check'),
               ('Проверить текст на уникальность в text.ru', 'unique'),
               ('Проверить текст на уникальность в сontent_watch', 'content_watch'),
               ('Проверить текст на в Turgenev', 'turgenev'),
               ('Получить ID товаров в МВидео', 'get_ids'),
               ('Загрузить чек', 'receipt'),
               ('Тексты за этот месяц', 'history'),
               ('Тексты за прошлый месяц', 'last_month'),
               ('Все твои тексты с ноября 2023', 'all_texts'),
               ('Свободные брифы', 'free_texts'),
               (f'{"Хочу снова работать!!!" if vacation[0]["vacation"] else "Иду в отпуск"}', 'vacation')]

    markup = create_markup(buttons)
    await message.answer("⬇⬇⬇ Ультимативный гайд для авторов GameGuru ⬇⬇⬇", reply_markup=markup)
