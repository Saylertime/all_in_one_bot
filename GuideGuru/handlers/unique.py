from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from utils.docs import get_content, check_text
from utils.text_ru import text_unique_check, symbols_left
from psql_maker import find_author


router_unique = Router()


class UniqueState(StatesGroup):
    response = State()


@router_unique.callback_query(F.data == "unique")
@router_unique.message(Command("unique"))
async def unique(message, state):
    username = "@" + message.from_user.username
    if isinstance(message, CallbackQuery):
        message = message.message

    name_in_db = await find_author(username)
    if name_in_db:
        msg = ('Введи ссылку в формате \n\n'
               'https://docs.google.com/document/d/'
               '1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit')
        await state.set_state(UniqueState.response)
        await message.answer(msg)
    else:
        await message.answer(f"{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил",
                         parse_mode="HTML")


@router_unique.message(F.text, UniqueState.response)
async def unique_answer(message, state):
    await state.clear()
    try:
        url = message.text.split("/")[5]
        full_text = await get_content(url)
        msg = await check_text(url) + "\n\n _____________________ \n\n"
        left_symbs = await symbols_left()
        symb = int(left_symbs.replace(",", ""))
        if not len(full_text) > symb:
            await message.answer("Нужно подождать..... Если текст большой, проверка займёт пару минут")
            result = await text_unique_check(full_text)
            msg += str(result)
            if len(msg) > 3999:
                await message.answer(
                                 "Очень много ссылок, откуда скопировано. Я не резиновый, чтобы все их вывести...")
            else:
                await message.answer(msg)
        else:
            await message.answer("У меня заканчиваются символы, извени(((99")

    except Exception as error:
        await message.answer("Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования")
        error = str(error) + f"\n\n{message.from_user.username}\n\n{message.text}"
