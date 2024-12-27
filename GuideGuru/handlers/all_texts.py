from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile

from utils.sheets import all_texts_of_author
from psql_maker import find_author


router_all_text = Router()


@router_all_text.callback_query(F.data == "all_texts")
@router_all_text.message(Command("all_texts"))
async def all_texts(message):
    username = "@" + message.from_user.username
    if isinstance(message, CallbackQuery):
        message = message.message

    name_in_db = await find_author(username)

    if name_in_db:
        all_texts_eldo, all_texts_mvideo = await all_texts_of_author(name_in_db)

        if all_texts_eldo:
            file_to_send = FSInputFile(all_texts_eldo)
            await message.answer_document(file_to_send)

        if all_texts_mvideo:
            file_to_send = FSInputFile(all_texts_mvideo)
            await message.answer_document(file_to_send)

        if not all_texts_eldo and not all_texts_mvideo:
            msg = "Ничего не нашел. У тебя точно есть тексты?"
            await message.answer(msg)

    else:
        msg = f' {username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил'
        await message.answer(msg, parse_mode='HTML')
