from aiogram import Router
from aiogram.filters import Command

from states.overall import OverallState
from utils.sheets import rep_month


router_money = Router()


@router_money.message(Command("money"))
async def money(message, state):
    await message.answer("Введи месяц и год в формате 'Январь 2024'")
    await state.set_state(OverallState.money)


@router_money.message(OverallState.money)
async def answer(message, state):
    await state.clear()
    msg = await rep_month(message.text)
    await message.answer(msg)
