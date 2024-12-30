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


@router_history.message(OverallState.history)
async def answer(message, state):
    await state.clear()
    try:
        split_message = message.text.split(", ")
        name = split_message[0]
        current_month = split_message[1]
        msg = await rep_name_and_month(name=name, month=current_month)
        await message.answer(msg, parse_mode="HTML")
    except:
        await message.answer("Введи нормально :(")
