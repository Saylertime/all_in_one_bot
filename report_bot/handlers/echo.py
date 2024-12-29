from aiogram import Router, F
import aiofiles

from pg_maker import delete_author
from utils.sheets import rep_name_and_month_sber


router_echo = Router()


@router_echo.message(F.text.lower() == "история")
async def history_log(message):
    async with aiofiles.open('bot.log', mode='r') as file:
        lines = await file.readlines()
        msg = "\n".join(lines[-30:])
        await message.answer(f"{msg}")


@router_echo.message(F.text.startswith("удалить"))
async def delete_author_func(message):
    try:
        name = message.text.split(" ")[1]
        result = await delete_author(name)
        if result:
            await message.answer(f"Мы будем скучать по тебе, {name} ;(")
        else:
            await message.answer(f"Такого нет. Может, мы его выперли уже давно?")
    except Exception as e:
        await message.answer(f"Такого нет. Может, мы его выперли уже давно?\n\n{e}")


@router_echo.message(F.text == "сбер")
async def sber_func(message):
    from utils.calendar import last_month
    data = await rep_name_and_month_sber(month=last_month())
    await message.answer(str(data))


@router_echo.message(F.text == "СБЕР")
async def new_sber_func(message):
    data = await rep_name_and_month_sber()
    await message.answer(str(data))


@router_echo.message(~F.text.startswith("/"))
async def echo_echo(message):
    await message.reply(f"Такой команды нет: {message.text}\n"
                        f"Нажмите /start, чтобы посмотреть весь список команд")
