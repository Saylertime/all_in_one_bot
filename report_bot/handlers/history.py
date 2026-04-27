from aiogram import Router
from aiogram.filters import Command

from states.overall import OverallState
from utils.sheets import rep_name_and_month


router_history = Router()


@router_history.message(Command("history"))
async def history(message, state):
    await message.answer(
        "Введи имя автора (как в таблице) и через запятую месяц и год. Пример:"
        "\n\nПаша, Январь 2024"
    )
    await state.set_state(OverallState.history)


from aiogram.types import FSInputFile

@router_history.message(OverallState.history)
async def answer(message, state):
    await state.clear()
    try:
        name, current_month = message.text.split(", ", 1)
        result = await rep_name_and_month(name=name, month=current_month)

        if result and result.endswith(".txt"):
            await message.answer_document(FSInputFile(result))
        else:
            await message.answer(result or "Данных не найдено", parse_mode="HTML")

    except Exception as e:
        await message.answer(f"Введи нормально :( Ошибка: {e}")
