from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from filters.is_author import IsAuthorFilter
from keyboards.reply.create_markup import create_markup_with_url


router_mvideo = Router()


@router_mvideo.callback_query(F.data == "mvideo", IsAuthorFilter())
@router_mvideo.message(Command("mvideo"), IsAuthorFilter())
async def mvideo(message):
    if isinstance(message, CallbackQuery):
        message = message.message

    buttons = [
        (
            "Каталог товаров одной категории",
            "https://docs.google.com/document/d/1UKrq_lVZmv0fqDXXdeupH4DSDIW4g4R7t_V_JmIuIz0/edit",
            None,
        ),
        (
            "Каталог товаров разных категорий одной темы",
            "https://docs.google.com/document/d/1aadfoGBtNFN7ZTx5hOyeh89VI3SZOOgnD3kfn18KEF8/edit",
            None,
        ),
        (
            "Подборка игр",
            "https://docs.google.com/document/d/1pcIlUSNWk-62G-BlS3fyyqhssH0WiBBnqKl1A6HY_wE/edit",
            None,
        ),
        (
            "Подборка фильмов",
            "https://docs.google.com/document/d/1kiAr4ETNsUPuNovSo98qV-WA9XA3C9CSJsUYowN1kiU/edit",
            None,
        ),
        (
            "Интервью",
            "https://docs.google.com/document/d/1_wxmmUsdsF_-qcwMNIvgDfA5P4cAqU4w-ifYF0Yk7eU/edit",
            None,
        ),
        (
            "Разговор с экспертом",
            "https://docs.google.com/document/d/1pGF-Rx8F43oC5Snve16aLosElvnIUpzSU2lFIYvXDks/edit",
            None,
        ),
        (
            "Каталог товаров с историями",
            "https://docs.google.com/document/d/11QAE5ttI-RHvZDSUV7EsY_lEki9Elxow6W-szbpWUwg/edit",
            None,
        ),
        (
            "Обзор фильма",
            "https://docs.google.com/document/d/1zn7v4I7K8pz5KlL_5o2b_ndWSHTlTBsutSN-5C-ZiPw/edit",
            None,
        ),
        (
            "Что известно об игре",
            "https://docs.google.com/document/d/1XE55X60f0nZqoKArbt8iwgucjSUrbuLkGjdFMxgtW50/edit",
            None,
        ),
        (
            "Советы, помощь, инструкции, пояснения",
            "https://docs.google.com/document/d/1K-Q6KAE4IB43hwKdfp5vnrP4FvckPUc8LfJ9_Iy0cRc/edit",
            None,
        ),
        (
            "Подарки",
            "https://docs.google.com/document/d/1m6o80ymYaZ0J2tVvGrBX7O-l550S4sEumpU63F4LQ6Y/edit",
            None,
        ),
        (
            "Обзор смартфона",
            "https://docs.google.com/document/d/1jNJVwLrcpmbqJ9vePuAPI687OvVH_wUro7cyQ0zpSms/edit#heading=h.v0yq6ffiv0uq",
            None,
        ),
        ("⬆⬆⬆ НАЗАД В МЕНЮ ⬆⬆⬆", None, "start"),
    ]
    markup = create_markup_with_url(buttons)
    await message.answer("Мклик", reply_markup=markup)
