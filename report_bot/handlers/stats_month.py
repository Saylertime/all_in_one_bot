from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from utils.sheets import stats_for_month


router_stats_month = Router()


class StatsMonthState(StatesGroup):
    response = State()


@router_stats_month.message(Command("stats_month"))
async def stats_month(message, state):
    await message.answer(
        "Введи месяц с большой буквы и год через пробел. Пример:" "\n\nЯнварь 2024"
    )
    await state.set_state(StatsMonthState.response)


@router_stats_month.message(F.text, StatsMonthState.response)
async def answer(message, state):
    await state.clear()
    try:
        month = str(message.text)
        msg = await stats_for_month(month)
        await message.answer(msg)
    except Exception as e:
        await message.answer(f"Скорее всего, что-то не так ввели\n\n{e}")
