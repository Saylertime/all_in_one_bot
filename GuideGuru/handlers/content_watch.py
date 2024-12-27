from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from utils.content_watch import content_watch_check
from utils.docs import get_content, check_text
from psql_maker import find_author


router_content_watch = Router()


class WatchState(StatesGroup):
    response = State()


@router_content_watch.callback_query(F.data == "content_watch")
@router_content_watch.message(Command("content_watch"))
async def content_watch(message, state):
    username = "@" + message.from_user.username
    if isinstance(message, CallbackQuery):
        message = message.message

    name_in_db = await find_author(username)
    if name_in_db:
        msg = ("Введи ссылку в формате \n\n"
               "https://docs.google.com/document/d/"
               "1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit")
        await state.set_state(WatchState.response)
    else:
        msg = f"{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил"
    await message.answer(msg)


@router_content_watch.message(F.text, WatchState.response)
async def content_watch_answer(message, state):
    await state.clear()
    try:
        url = message.text.split("/")[5]
        full_text = await get_content(url)
        first_check = await check_text(url)
        msg = first_check + "\n\n _____________________ \n\n"
        await message.answer("Нужно подождать..... Если текст большой, проверка займёт пару минут")
        checking = await content_watch_check(full_text)
        msg += checking
        if len(msg) > 3999:
            await message.answer("Очень много ссылок, откуда скопировано. Я не резиновый, чтобы все их вывести...")
        else:
            await message.answer(msg)
    except Exception as error:
        await message.answer("Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования")
        error = str(error) + f"\n\n{message.from_user.username}\n\n{message.text}"
        await message.answer(error)
