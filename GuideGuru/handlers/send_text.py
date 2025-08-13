from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from config_data import config
from filters.is_author import IsAuthorFilter
from loader import bot
from states.overall import OverallState
from utils.docs import check_text, get_content
from utils.text_ru import text_unique_check
from utils.turgenev import check_text_in_turgenev
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
        if "Стоп-слов нет, ты молодчуля ;)" in answer:
            with open("texts.txt", "a") as file:
                file.write(str(datetime.today()) + " " + message.text + " " + author + " @" + message.from_user.username + "\n")

            for admin in admins:
                await bot.send_message(admin, author_msg + message.text)
            await message.answer("Всё хорошо, текст ушёл на проверку!")

            try:
                full_text = await get_content(url)
                result_turgenev = await check_text_in_turgenev(full_text["full_text"])
                result_unique = await text_unique_check(full_text["full_text"])
                result = result_turgenev + "\n\n" + result_unique

                for admin in admins:
                    if len(result) < 4000:
                        await bot.send_message(admin, result)
            except Exception as e:
                print(e)
        else:
            msg = "<b>ИСПРАВЬ НЕПОТРЕБСТВА И ПОВТОРИ ПОПЫТКУ!!!</b>\n\n"
            await message.answer(msg + answer, parse_mode="HTML")
    except Exception as e:
        print(e)
        await message.answer(
            "Похоже, ссылкая кривая, не тот формат или доступ для редактирования закрыт"
        )
