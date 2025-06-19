from filters.is_author import IsAuthorFilter
from psql_maker import author_on_vacation, update_author_with_id
from keyboards.reply.create_markup import create_markup_with_url
from config_data import config

from aiogram import F, Router
from aiogram.filters import CommandStart

router_start = Router()
admins = config.ADMINS


async def handle_start(message, edit=False):
    await update_author_with_id(
        user_id=str(message.from_user.id), nickname=f"@{message.from_user.username}"
    )
    vacation = await author_on_vacation(message.from_user.username)
    if edit:
        message = message.message

    buttons = [
        ("Wiki гуравторов",
         "https://octagonal-roadway-041.notion.site/1d98f2cd29ea806b978ad969d9cc5445?v=1d98f2cd29ea8016beb6000c23dbf175",
            None),
        ("Отправить текст редактору", None, "send_text"),
        ("Задать вопрос по работе", None, "chatgpt"),
        ("Проверить текст на стоп-слова", None, "check"),
        ("Проверить текст на уникальность в text.ru", None, "unique"),
        ("Проверить текст на уникальность в content_watch", None, "content_watch"),
        ("Проверить текст на в Turgenev", None, "turgenev"),
        ("Получить ID товаров в МВидео", None, "get_ids"),
        ("Загрузить чек", None, "receipt"),
        ("Тексты за этот месяц", None, "history"),
        ("Тексты за прошлый месяц", None, "last_month"),
        ("Все твои тексты с ноября 2023", None, "all_texts"),
        ("Свободные брифы", None, "free_texts"),
        (
            f'{"Хочу снова работать!!!" if vacation[0]["vacation"] else "Иду в отпуск"}', None,
            "vacation",
        ),
    ]

    buttons_for_admins = [
        ("Оповещение", None, "button"),
        ("Посмотреть присланные тексты за день", None, "see_texts_one_day"),
        ("Посмотреть присланные тексты за период", None, "see_texts_period"),
    ]

    if str(message.from_user.id) in admins:
        for button in buttons_for_admins:
            buttons.append(button)

    markup = create_markup_with_url(buttons)

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
