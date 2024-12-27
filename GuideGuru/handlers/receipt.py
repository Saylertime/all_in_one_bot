from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

import re
from utils.receipt_sheets import get_data_from_sheet, new_list
from psql_maker import find_author


router_receipt = Router()


class ReceiptState(StatesGroup):
    response = State()


@router_receipt.callback_query(F.data == "receipt")
@router_receipt.message(Command("receipt"))
async def receipt(message, state):
    username = "@" + message.from_user.username
    if isinstance(message, CallbackQuery):
        message = message.message

    name_in_db = await find_author(username)
    if name_in_db:
        await state.set_state(ReceiptState.response)
        await message.answer("Закинь сюда ссылку на чек. Больше ничего не надо — ни имени, ни месяца")
    else:
        await message.answer("Тебя нет в базе данных... Обратись к @saylertime, чтобы он порешал")


@router_receipt.message(F.text, ReceiptState.response)
async def upload_link(message, state):
    await state.clear()
    if contains_ru_domain(message.text):
        full_name = await get_data_from_sheet(message.from_user.username)
        await new_list(full_name, message.text)
        await message.answer("Спасибо, всё получилось")
    else:
        await message.answer("Это точно ссылка? Не вижу в ней .ru. Начни всё заново /receipt")


def contains_ru_domain(url):
    ru_pattern = re.compile(r'\.ru\b', re.IGNORECASE)
    return re.search(ru_pattern, url) is not None
