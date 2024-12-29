from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from utils.docs import get_content
from utils.turgenev import check_text_in_turgenev
from psql_maker import find_author


router_turgenev = Router()


class TurgenevState(StatesGroup):
    response = State()


@router_turgenev.callback_query(F.data == "turgenev")
@router_turgenev.message(Command("turgenev"))
async def turgenev(message, state):
    username = "@" + message.from_user.username
    if isinstance(message, CallbackQuery):
        message = message.message

    name_in_db = await find_author(username)
    await message.answer(str(name_in_db))
    if name_in_db:
        msg = (
            "Введи ссылку в формате \n\n"
            "https://docs.google.com/document/d/1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit\n\n"
            "Критерии оценки: \n"
            "<b>До 5 баллов</b> — все хорошо\n"
            "<b>5-8 баллов</b> — средний риск\n"
            "<b>8-13</b> — нужно что-то делать\n"
            "<b>13+</b> – критическая ситуация."
        )
        await state.set_state(TurgenevState.response)
        await message.answer(msg)
    else:
        await message.answer(
            f"{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил",
            parse_mode="HTML",
        )


@router_turgenev.message(F.text, TurgenevState.response)
async def turgenev_answer(message, state):
    await state.clear()
    try:
        url = message.text.split("/")[5]
        full_text = await get_content(url)
        await message.answer(
            "Нужно подождать..... Если текст большой, проверка займёт пару минут"
        )
        result = await check_text_in_turgenev(full_text)
        await message.answer(result, parse_mode="HTML")

    except Exception as error:
        await message.answer(
            f"Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования\n\n {error}"
        )
