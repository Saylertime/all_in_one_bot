from aiogram import Router
from aiogram.filters import Command

from utils.sheets import who_is_free
from pg_maker import authors_on_vacation


router_free_authors = Router()


@router_free_authors.message(Command("free_authors"))
async def free_authors_func(message):
    free_authors, authors_with_text, authors_with_few_texts = await who_is_free()
    on_vacation = await authors_on_vacation()

    if free_authors:
        msg = "Сейчас свободны: \n\n"
        for author in free_authors:
            msg += f"{author[1]} — {author[0]}\n"

        msg += "\nАвторы с одним текстом: \n\n"
        for author in authors_with_text:
            msg += f"{author[1]} — {author[0]}\n"

        msg += "\nОчень занятые авторы: \n\n"
        for author in authors_with_few_texts:
            msg += f"{author[1]} — {author[0]}\n"

        if on_vacation:
            msg += "\nАвторы в отпуске: \n\n"
            for author in on_vacation:
                msg += f"{author[2]} — {author[1]}\n"
        await message.answer(msg)

    else:
        await message.answer("Все такие занятые, я прям не могу(((")
