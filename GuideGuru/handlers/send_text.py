from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from config_data import config
from filters.is_author import IsAuthorFilter
from loader import bot
from states.overall import OverallState
from utils.docs import check_text
from psql_maker import find_author
from datetime import datetime


router_send_text = Router()
admins = config.ADMINS


@router_send_text.message(Command("send_text"), IsAuthorFilter())
@router_send_text.callback_query(F.data == "send_text")
async def send_text(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message

    msg = (
        "Кидай ссылку на документ, который надо отправить.\n\n"
        "Не забудь открыть доступ"
    )

    await message.answer(msg)
    await state.set_state(OverallState.send_text)


@router_send_text.message(OverallState.send_text)
async def send_answer(message, state):
    await state.clear()
    author = await find_author("@" + message.from_user.username)
    author_msg = f"{author} (@{message.from_user.username}) прислал текст \n\n"
    try:
        url = message.text.split("/")[-2]
        answer = await check_text(url, is_check_for_admins=True)
        if answer == "Стоп-слов нет, ты молодчуля ;)":
            with open("texts.txt", "a") as file:
                file.write(str(datetime.today()) + " " + message.text + " " + author + " @" + message.from_user.username + "\n")

            for admin in admins:
                await bot.send_message(admin, author_msg + message.text)
            await message.answer("Всё хорошо, текст ушёл на проверку!")
        else:
            msg = "<b>ИСПРАВЬ НЕПОТРЕБСТВА И ПОВТОРИ ПОПЫТКУ!!!</b>\n\n"
            await message.answer(msg + answer, parse_mode="HTML")
    except Exception as e:
        print(e)
        await message.answer(
            "Похоже, ссылкая кривая, не тот формат или доступ для редактирования закрыт"
        )
