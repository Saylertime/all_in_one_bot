from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from utils.docs import check_text


router_check = Router()


class CheckState(StatesGroup):
    response = State()


@router_check.message(Command('check'))
@router_check.callback_query(F.data == "check")
async def check(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message

    msg = ("Кидай ссылку на документ, который надо проверить.\n\n"
           "Ссылка должна выглядеть так.\n\n"
           "https://docs.google.com/document/d/136QHaIF8G_w6fJzTJIstoA0sKRwNElsTAzzXyJ0xwj8/edit")

    await message.answer(msg)
    await state.set_state(CheckState.response)


@router_check.message(F.text, CheckState.response)
async def check_answer(message, state):
    await state.clear()
    try:
        url = message.text.split('/')[-2]
        answer = await check_text(url)
        await message.answer(answer)
    except:
        await message.answer('Похоже, ссылкая кривая, не тот формат или доступ для редактирования закрыт')
