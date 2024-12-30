from aiogram import Router, F
from aiogram.filters import Command

from handlers.start import handle_start
from filters.is_author import IsAuthorFilter
from config_data import config
from loader import bot
from psql_maker import author_on_vacation, update_vacation_status, find_author


admins = config.ADMINS
router_vacation = Router()


async def handle_vacation(message):
    username = "@" + message.from_user.username
    name_in_db = await find_author(username)
    vacation = await author_on_vacation(username[1:])
    vacation_status = vacation[0]["vacation"] if vacation else False
    new_status = not vacation_status
    await update_vacation_status(username[1:], new_status)
    await message.answer(
        f'Теперь ты {"в отпуске" if new_status else "снова работаешь"}!'
    )

    msg = f"{name_in_db} {'в отпуске' if new_status else 'снова в строю'}"
    for admin in admins:
        await bot.send_message(admin, msg)


@router_vacation.callback_query(F.data == "vacation", IsAuthorFilter())
async def vacation_callback(message):
    await handle_vacation(message)
    await handle_start(message, edit=True)


@router_vacation.message(Command("vacation"), IsAuthorFilter())
async def vacation_text(message):
    await handle_vacation(message)
