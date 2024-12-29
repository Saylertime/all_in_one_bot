import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile

from psql_maker import find_author
from utils.calend import previous_month, current_month
from utils.sheets import rep_name_and_month, rep_name_and_month_sber


router_history = Router()


@router_history.callback_query(
    lambda callback: callback.data in ["history", "last_month"]
)
@router_history.message(Command(commands=["history", "last_month"]))
async def history(message):
    username = "@" + message.from_user.username
    if isinstance(message, CallbackQuery):
        callback = message
        message = callback.message
        month = current_month() if callback.data == "history" else previous_month()
    else:
        message = message
        month = current_month() if message.text == "/history" else previous_month()

    name_in_db = await find_author(username)

    if not name_in_db:
        await message.answer(
            f"{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил"
        )
        return

    sber_data = await rep_name_and_month_sber(name_in_db, month=month)
    msg = await rep_name_and_month(name_in_db, month=month, sber_data=sber_data)

    if os.path.isfile(msg):
        file = FSInputFile(msg)
        await message.answer_document(file)
    else:
        await message.answer(msg)
