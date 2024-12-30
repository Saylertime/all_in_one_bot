from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from filters.is_author import IsAuthorFilter
from states.overall import OverallState
from utils.docs import get_content, check_text
from utils.text_ru import text_unique_check, symbols_left


router_unique = Router()


@router_unique.callback_query(F.data == "unique", IsAuthorFilter())
@router_unique.message(Command("unique"), IsAuthorFilter())
async def unique(message, state):
    if isinstance(message, CallbackQuery):
        message = message.message

    msg = (
        "Введи ссылку в формате \n\n"
        "https://docs.google.com/document/d/"
        "1Q33XaT68BhrUPYPkOQPuzTZCATiNn0QnV3bxu74_bug/edit"
    )
    await state.set_state(OverallState.unique)
    await message.answer(msg)


@router_unique.message(OverallState.unique)
async def unique_answer(message, state):
    await state.clear()
    try:
        url = message.text.split("/")[5]
        full_text = await get_content(url)
        msg = await check_text(url) + "\n\n _____________________ \n\n"
        left_symbs = await symbols_left()
        symb = int(left_symbs.replace(",", ""))
        if not len(full_text) > symb:
            await message.answer(
                "Нужно подождать..... Если текст большой, проверка займёт пару минут"
            )
            result = await text_unique_check(full_text)
            msg += str(result)
            if len(msg) > 3999:
                await message.answer(
                    "Очень много ссылок, откуда скопировано. Я не резиновый, чтобы все их вывести..."
                )
            else:
                await message.answer(msg)
        else:
            await message.answer("У меня заканчиваются символы, извени(((99")

    except Exception as error:
        await message.answer(
            "Похоже, ссылкая кривая, не тот формат или закрыт доступ для редактирования"
        )
        error = str(error) + f"\n\n{message.from_user.username}\n\n{message.text}"
