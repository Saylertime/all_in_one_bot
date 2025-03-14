from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from filters.is_author import IsAuthorFilter
from states.overall import OverallState
from utils.docs import get_content
from utils.turgenev import check_text_in_turgenev


router_turgenev = Router()


@router_turgenev.callback_query(F.data == "turgenev", IsAuthorFilter())
@router_turgenev.message(Command("turgenev"), IsAuthorFilter())
async def turgenev(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message
    msg = (
        "Введи ссылку в формате \n\n"
        "https://docs.google.com/document/d/1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit\n\n"
        "Критерии оценки: \n"
        "<b>До 5 баллов</b> — все хорошо\n"
        "<b>5-8 баллов</b> — средний риск\n"
        "<b>8-13</b> — нужно что-то делать\n"
        "<b>13+</b> – критическая ситуация."
    )
    await state.set_state(OverallState.turgenev)
    await message.answer(msg)


@router_turgenev.message(OverallState.turgenev)
async def turgenev_answer(message, state):
    await state.clear()
    try:
        url = message.text.split("/")[5]
        full_text = await get_content(url)
        await message.answer(
            "Нужно подождать..... Если текст большой, проверка займёт пару минут"
        )
        result = await check_text_in_turgenev(full_text["full_text"])
        await message.answer(result, parse_mode="HTML")

    except Exception as error:
        await message.answer(
            f"Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования\n\n {error}"
        )
