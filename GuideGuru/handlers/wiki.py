from aiogram.filters import Command
from aiogram import Router
from keyboards.reply.create_markup import create_markup_with_url

router_wiki = Router()

WIKI_URL = "https://octagonal-roadway-041.notion.site/1d98f2cd29ea806b978ad969d9cc5445?v=1d98f2cd29ea8016beb6000c23dbf175"


@router_wiki.message(Command("wiki"))
async def wiki_command(message):
    markup = create_markup_with_url([
        ("Открыть Wiki", WIKI_URL, None),
    ])
    await message.answer(
        "Наша Wiki:",
        reply_markup=markup
    )
