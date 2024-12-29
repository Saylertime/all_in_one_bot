from aiogram import Router
from aiogram.filters import Command

from utils.sheets import in_work_today


router_deadlines = Router()


@router_deadlines.message(Command("deadlines"))
async def deadlines(message):
    msg = await in_work_today()
    await message.answer(msg, parse_mode="HTML")
