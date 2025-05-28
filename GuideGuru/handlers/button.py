from aiogram import Router, F
from aiogram.filters import Command

from keyboards.reply.create_markup import create_markup
from utils.sheets import brief_is_free
from psql_maker import all_authors_without_anything
from loader import bot
from filters.is_author import IsAuthorFilter
from handlers.free_texts import split_message_by_paragraphs


router_button = Router()


@router_button.callback_query(F.data == "button", IsAuthorFilter())
@router_button.message(Command("button"), IsAuthorFilter())
async def button(message):
    authors = await all_authors_without_anything()
    free_briefs = await brief_is_free()
    if free_briefs:
        messages = split_message_by_paragraphs(f"Мы добавили новые брифы! "
                                               f"На момент появления этого сообщения, появились такие задачи: "
                                               f"\n\n{free_briefs}")

    else:
        messages = ["Всё разобрали! Ждём новых поступлений"]

    markup_buttons = [("Обновить список", "free_texts")]
    markup = create_markup(buttons=markup_buttons, columns=1)
    for author in authors:
        try:
            for msg in messages:
                await bot.send_message(
                    chat_id=int(author["user_id"]),
                    text=msg,
                    parse_mode="Markdown",
                    disable_web_page_preview=True,
                    reply_markup=markup
                )
        except Exception as e:
            print(e)
