from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile

from states.overall import OverallState
from utils.sheets import all_texts_of_author


router_all_texts = Router()


@router_all_texts.message(Command("all_texts"))
async def all_texts(message, state):
    await message.answer("Введи имя автора (как в таблице) Пример:" "\n\nПаша")
    await state.set_state(OverallState.all_texts)


@router_all_texts.message(OverallState.all_texts)
async def answer(message, state):
    await state.clear()
    all_texts_eldo, all_texts_mvideo = await all_texts_of_author(message.text)
    if all_texts_eldo:
        file_to_send = FSInputFile(all_texts_eldo)
        await message.answer_document(file_to_send)

    if all_texts_mvideo:
        file_to_send = FSInputFile(all_texts_mvideo)
        await message.answer_document(file_to_send)

    if not all_texts_eldo and not all_texts_mvideo:
        msg = "Ничего не нашел. У него точно есть тексты?"
        await message.answer(msg)
