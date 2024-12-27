from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from utils.docs import get_content_with_links
import re


router_get_ids = Router()


class GetState(StatesGroup):
    response = State()


@router_get_ids.callback_query(F.data == "get_ids")
@router_get_ids.message(Command("get_ids"))
async def get_ids(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message

    await message.answer("Кидай ссылку на документ, из которого надо достать ID.\n\n"
                   "Ссылка должна выглядеть так.\n\n"
                   "https://docs.google.com/document/d/136QHaIF8G_w6fJzTJIstoA0sKRwNElsTAzzXyJ0xwj8/edit")
    await state.set_state(GetState.response)


@router_get_ids.message(F.text, GetState.response)
async def get_ids_answer(message, state):
    await state.clear()
    try:
        url = message.text.split("/")[-2]
        links = await get_content_with_links(url)
        if links:
            await message.answer(str(get_product_ids(links)))
        else:
            await message.answer("Кажется, ссылок нет")
    except Exception as e:
        await message.answer(f"Похоже, ссылкая кривая, не тот формат или доступ для редактирования закрыт\n\n {e}")


def get_product_ids(content):
    pattern = r"https://www\.mvideo\.ru/products/[a-zA-Z0-9\-\_]+-\d+"
    links = [link for link in content if re.match(pattern, link)]
    if links:
        ids = set([link.split('-')[-1] for link in links])
        return ", ".join(ids)
