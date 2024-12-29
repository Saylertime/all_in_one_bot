from aiogram import Router
from aiogram.filters import Command

from pg_maker import all_authors


router_authors = Router()


@router_authors.message(Command("authors"))
async def all_authors_func(message):
    msg = ''
    authors = await all_authors()
    if authors:
        for author in authors:
            msg += f"{author[0]} — {author[1]}. В таблице: {author[2]}\n\n"
        print(authors)
    else:
        msg = 'Что-то с базой данных ;('
    await message.answer(msg)
