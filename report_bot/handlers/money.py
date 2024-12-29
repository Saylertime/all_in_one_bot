from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from utils.sheets import rep_month


router_money = Router()


class MoneyState(StatesGroup):
    response = State()


@router_money.message(Command("money"))
async def money(message, state):
    await message.answer("Введи месяц и год в формате 'Январь 2024'")
    await state.set_state(MoneyState.response)


@router_money.message(F.text, MoneyState.response)
async def answer(message, state):
    await state.clear()
    msg = await rep_month(message.text)
    await message.answer(msg)
