from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery

from filters.is_author import IsAuthorFilter
from utils.sheets import brief_is_free


router_free_texts = Router()


@router_free_texts.callback_query(F.data == "free_texts", IsAuthorFilter())
@router_free_texts.message(Command("free_texts"), IsAuthorFilter())
async def free_texts(message):
    if isinstance(message, CallbackQuery):
        message = message.message

    free_briefs = await brief_is_free()

    if free_briefs:
        messages = split_message_by_paragraphs(
            f"Сейчас свободны: \n\n{free_briefs}"
        )
        for msg in messages:
            await message.answer(
                msg, parse_mode="Markdown", disable_web_page_preview=True
            )
    else:
        await message.answer(
            "Всё разобрали! Ждём новых поступлений",
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )


def split_message_by_paragraphs(message, max_length=4500):
    parts = []
    current_part = ""

    paragraphs = message.split("\n\n")

    for paragraph in paragraphs:
        if len(current_part) + len(paragraph) + 2 <= max_length:
            current_part += paragraph + "\n\n"
        else:
            parts.append(current_part.strip())
            current_part = paragraph + "\n\n"

    if current_part.strip():
        parts.append(current_part.strip())

    return list(dict.fromkeys(parts))
