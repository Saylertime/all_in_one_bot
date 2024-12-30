from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

import re
from filters.is_author import IsAuthorFilter
from states.overall import OverallState
from utils.receipt_sheets import get_data_from_sheet, new_list


router_receipt = Router()


@router_receipt.callback_query(F.data == "receipt", IsAuthorFilter())
@router_receipt.message(Command("receipt"), IsAuthorFilter())
async def receipt(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message

    await state.set_state(OverallState.receipt)
    await message.answer(
        "Закинь сюда ссылку на чек. Больше ничего не надо — ни имени, ни месяца"
    )


@router_receipt.message(OverallState.receipt)
async def upload_link(message, state):
    await state.clear()
    if contains_ru_domain(message.text):
        full_name = await get_data_from_sheet(message.from_user.username)
        await new_list(full_name, message.text)
        await message.answer("Спасибо, всё получилось")
    else:
        await message.answer(
            "Это точно ссылка? Не вижу в ней .ru. Начни всё заново /receipt"
        )


def contains_ru_domain(url):
    ru_pattern = re.compile(r"\.ru\b", re.IGNORECASE)
    return re.search(ru_pattern, url) is not None
