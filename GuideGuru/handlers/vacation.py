from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from config_data import config
from loader import bot
from psql_maker import author_on_vacation, update_vacation_status, find_author


admins = config.ADMINS
router_vacation = Router()


@router_vacation.callback_query(F.data == "vacation")
@router_vacation.message(Command("vacation"))
async def vacation_func(message):
    username = "@" + message.from_user.username

    if isinstance(message, CallbackQuery):
        message = message.message

    name_in_db = await find_author(username)

    if name_in_db:
        vacation = await author_on_vacation(username[1:])
        vacation_status = vacation[0]["vacation"] if vacation else False
        new_status = not vacation_status
        await update_vacation_status(username[1:], new_status)
        await message.answer(f'Теперь ты {"в отпуске" if new_status else "снова работаешь"}!')

        msg = f"{name_in_db} {'в отпуске' if new_status else 'снова в строю'}"
        for admin in admins:
            await bot.send_message(admin, msg)

    else:
        await message.answer(
            f"{username}, тебя пока нет в базе данных ;( Напиши @saylertime, чтобы добавил",
            parse_mode="HTML"
        )
