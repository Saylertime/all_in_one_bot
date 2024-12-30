from filters.is_author import IsAuthorFilter
from psql_maker import author_on_vacation
from keyboards.reply.create_markup import create_markup


from aiogram import F, Router
from aiogram.filters import CommandStart

router_start = Router()


async def handle_start(message, edit=False):
    vacation = await author_on_vacation(message.from_user.username)
    if edit:
        message = message.message

    buttons = [
        ("Правила оформления Эльдо", "eldo"),
        ("Правила оформления МВидео", "mvideo"),
        ("Проверить текст на стоп-слова", "check"),
        ("Проверить текст на уникальность в text.ru", "unique"),
        ("Проверить текст на уникальность в content_watch", "content_watch"),
        ("Проверить текст на в Turgenev", "turgenev"),
        ("Получить ID товаров в МВидео", "get_ids"),
        ("Загрузить чек", "receipt"),
        ("Тексты за этот месяц", "history"),
        ("Тексты за прошлый месяц", "last_month"),
        ("Все твои тексты с ноября 2023", "all_texts"),
        ("Свободные брифы", "free_texts"),
        (
            f'{"Хочу снова работать!!!" if vacation[0]["vacation"] else "Иду в отпуск"}',
            "vacation",
        ),
    ]

    markup = create_markup(buttons)

    if edit:
        await message.edit_text(
            "⬇⬇⬇ Ультимативный гайд для авторов GameGuru ⬇⬇⬇", reply_markup=markup
        )
    else:
        await message.answer(
            "⬇⬇⬇ Ультимативный гайд для авторов GameGuru ⬇⬇⬇", reply_markup=markup
        )


@router_start.message(CommandStart(), IsAuthorFilter())
async def start_message(message):
    await handle_start(message)


@router_start.callback_query(F.data == "start", IsAuthorFilter())
async def start_callback(callback):
    await handle_start(callback, edit=True)
