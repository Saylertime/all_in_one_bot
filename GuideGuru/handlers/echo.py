import aiofiles
import os
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile


from loader import bot
from filters.is_author import IsAuthorFilter
from keyboards.reply.create_markup import create_markup
from psql_maker import (
    new_table_stop_words,
    insert_new_word,
    delete_stop_word,
    all_stop_words,
    all_authors,
    find_author,
    update_money_status,
    update_money_status_for_everyone
)
from utils.text_ru import symbols_left
from utils.sheets import rep_name_and_month, rep_name_and_month_sber


router_echo = Router()


@router_echo.message(F.text.lower() == "зарплата")
async def gde_zarplata(message):
    authors = await all_authors()
    buttons = [("ДА!!!", "yes"), ("ЕЩЕ НЕТ((((", "no")]
    markup = create_markup(buttons)
    for author in authors:
        try:
            await bot.send_message(
                chat_id=int(author["user_id"]),
                text="Тебе уже пришел гонорар за этот месяц?",
                reply_markup=markup,
            )
        except Exception as e:
            print(e)


@router_echo.callback_query(F.data.in_({"yes", "no"}))
async def zarplata_pridet(callback):
    username = f"@{callback.from_user.username}"
    name_in_db = await find_author(username)
    flag = True

    if callback.data == "yes":
        msg = "Ура, мы и не сомневались!!"
        await update_money_status(username)

    else:
        msg = "Поняли, тормошим любимых бухов"
        flag = False

    msg_for_admins = f"{name_in_db} {'ПОКА НЕ' if not flag else 'УЖЕ'} получил зарплату"

    await callback.message.edit_text(msg)
    await bot.send_message(chat_id=68086662, text=msg_for_admins)


@router_echo.message(F.text.lower() == "zp")
async def got_zarplata(message):
    authors = await all_authors()
    buttons = [(name["name_in_db"], f"zp__{name['nickname']}") for name in authors]
    buttons.append(("Обнуление", "obnulenie"))
    markup = create_markup(buttons, columns=3)
    await message.answer("lol?", reply_markup=markup)


@router_echo.callback_query(F.data.startswith("zp__"))
async def change_salary(callback):
    nickname = callback.data.split("__")[1]
    await update_money_status(nickname)
    await callback.message.edit_text(f"{nickname} получил зарплату")
    await got_zarplata(callback.message)


@router_echo.callback_query(F.data.startswith("obnulenie"))
async def change_salary_obnulenie(callback):
    await update_money_status_for_everyone()
    await callback.message.edit_text("Никто не получил зарплату")
    await got_zarplata(callback.message)


@router_echo.message(F.text.lower() == "зп")
async def get_unpaid(message):
    authors = await all_authors()
    msg = "НЕ ПОЛУЧИЛИ: \n\n"
    for author in authors:
        msg += f"{author['name_in_db']} — {author['nickname']}\n"
    await message.answer(msg)


@router_echo.message(F.text.lower() == "история")
async def history_log(message):
    async with aiofiles.open("bot.log", mode="r") as file:
        lines = await file.readlines()
        filtered_lines = [
            line for line in lines if "@" in line and "история" not in line.lower()
        ]
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


@router_echo.message(F.text.lower().startswith("автор"))
async def author(message):
    name_in_db = message.text.split()[1]
    month = f"{message.text.split()[2]} {message.text.split()[3]}"
    sber_data = await rep_name_and_month_sber(name_in_db, month=month)
    msg = await rep_name_and_month(name_in_db, month=month, sber_data=sber_data)

    if os.path.isfile(msg):
        file = FSInputFile(msg)
        await message.answer_document(file)
    else:
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
