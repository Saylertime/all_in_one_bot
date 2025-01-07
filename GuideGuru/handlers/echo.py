import aiofiles
from aiogram import Router, F
from aiogram.types import CallbackQuery

from filters.is_author import IsAuthorFilter
from psql_maker import (
    new_table_stop_words,
    insert_new_word,
    delete_stop_word,
    all_stop_words,
)
from utils.text_ru import symbols_left


router_echo = Router()


@router_echo.message(F.text.lower() == "история")
async def history_log(message):
    async with aiofiles.open("bot.log", mode="r") as file:
        lines = await file.readlines()
        filtered_lines = [line for line in lines if "@" in line]
        msg = "\n".join(filtered_lines[-30:])
        await message.answer(f"{msg}")


@router_echo.message(F.text.lower() == "text")
async def text_left(message):
    symbs = await symbols_left()
    await message.answer(symbs)


@router_echo.message(F.text == "WORDS")
async def new_tab(message):
    await new_table_stop_words()
    await message.answer("Создана и обновлена")


@router_echo.message(F.text.startswith("ДОБАВИТЬ"))
async def add_word(message):
    word = str(message.text.split()[1])
    msg = await insert_new_word(word)
    await message.answer(msg)


@router_echo.message(F.text.startswith("УБРАТЬ"))
async def delete_word(message):
    word = str(message.text.split()[1])
    msg = await delete_stop_word(word)
    await message.answer(msg)


@router_echo.message(F.text.startswith("СТОП-СЛОВА"))
async def stop_words(message):
    msg = str(", ".join([i for i in await all_stop_words()]))[4000:]
    await message.answer(msg)


@router_echo.message(~IsAuthorFilter())
async def echo_not_author(message):
    if isinstance(message, CallbackQuery):
        message = message.message
    await message.reply(
        f"@{message.from_user.username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил",
        parse_mode="HTML",
    )


@router_echo.message(~F.text.startswith("/"))
async def echo_echo(message):
    await message.reply(
        f"Такой команды нет: {message.text}\n"
        f"Нажмите /start, чтобы посмотреть весь список команд"
    )
