from aiogram import Router
from aiogram.filters import Command

from states.overall import OverallState
from pg_maker import add_author


router_new_author = Router()


@router_new_author.message(Command("new_author"))
async def new_author(message, state):
    await message.answer(
        "Введи имя и фамилию автора, ник и то, как помечаем его в таблице. "
        "Всё через запятую с пробелом. Пример: \n\n"
        "Паша Ручкин, @pekron, Паша"
    )
    await state.set_state(OverallState.new_author)


@router_new_author.message(OverallState.new_author)
async def add_author_to_db(message, state):
    await state.clear()
    try:
        name, nickname, name_in_db = message.text.split(", ")
        await add_author(name, nickname, name_in_db)
        await message.answer(
            f"{nickname} добавлен!\n\n"
            f"Добавить еще одного — /new_author\n\n"
            f"Посмотреть всех — /authors"
        )
    except:
        pass
        await message.answer(
            f"Что-то не получилось. \n"
            f"Попробовать еще раз — /new_author\n"
            "Посмотреть всех — /authors"
        )
