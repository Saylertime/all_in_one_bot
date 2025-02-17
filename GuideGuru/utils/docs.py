import os
import asyncio
import aiofiles
from psql_maker import all_stop_words
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import HttpRequest

SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]


async def get_creds():
    creds = None
    if os.path.exists("token2.json"):
        creds = Credentials.from_authorized_user_file("token2.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            await asyncio.to_thread(creds.refresh, Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = await asyncio.to_thread(flow.run_local_server, port=0)
        async with aiofiles.open("token2.json", "w") as token:
            await token.write(creds.to_json())
    return creds


async def get_content(doc_id):
    try:
        creds = await get_creds()
        service = await asyncio.to_thread(build, "docs", "v1", credentials=creds)
        document = await asyncio.to_thread(
            service.documents().get(documentId=doc_id).execute
        )
        content = document.get("body").get("content")

        full_text = ""
        has_headings = False  # Флаг наличия заголовков
        colored_fragments = []

        for elem in content:
            paragraph = elem.get("paragraph")
            if paragraph:
                elements = paragraph.get("elements")
                paragraph_style = paragraph.get("paragraphStyle", {})

                # Проверяем, есть ли заголовки в документе
                if "namedStyleType" in paragraph_style:
                    if paragraph_style["namedStyleType"] in {
                        "HEADING_1",
                        "HEADING_2",
                        "HEADING_3",
                        "HEADING_4",
                        "HEADING_5",
                        "HEADING_6",
                    }:
                        has_headings = True

                for element in elements:
                    text_run = element.get("textRun")
                    if text_run:
                        text = text_run.get("content", "").strip()
                        if text:
                            full_text += f" {text}"
                        text_style = text_run.get("textStyle", {})

                        bg_color = None
                        if "backgroundColor" in text_style:
                            bg_color = (
                                text_style["backgroundColor"]
                                .get("color", {})
                                .get("rgbColor")
                            )

                        if bg_color:
                            colored_fragments.append(bg_color)

        return {
            "full_text": full_text,
            "has_headings": has_headings,
            "colored_fragments": True if len(colored_fragments) > 2 else False,
        }

    except Exception as e:
        print(e)
        return {"error": str(e)}


async def check_text(doc_id, is_content_watch=False):
    stop_words = await all_stop_words()
    content = await get_content(doc_id)
    all_content = content["full_text"]
    coloured_text = content["colored_fragments"]
    has_headings = content["has_headings"]

    stop_count = 0
    e_count = 0
    words = []
    msg = ""

    for word in all_content.split():
        if word.lower() in stop_words:
            words.append(word)
            stop_count += 1
        elif "ё" in word.lower() or "Ё" in word.lower():
            e_count += 1

    if stop_count == 0 and e_count == 0 and coloured_text:
        msg = "Стоп-слов нет, ты молодчуля ;)"

    elif stop_count:
        msg = f"Стоп-слов в тексте: {stop_count}. Вот они, слева направо:\n\n"
        msg += ", ".join(words)

    if e_count and not is_content_watch:
        msg += f"\n\nУбери буквы Ё. У тебя в тексте их {e_count}"

    if not coloured_text:
        msg += "\n\nЕсли это СЕО, то нужно выделить ключевики и LSI — их не хватает"

    if not has_headings:
        msg += "\n\nНе хватает оглавления"

    return msg


async def get_content_with_links(doc_id):
    try:
        creds = await get_creds()
        service = await asyncio.to_thread(build, "docs", "v1", credentials=creds)
        document = await asyncio.to_thread(
            service.documents().get(documentId=doc_id).execute
        )
        content = document.get("body").get("content")

        links = []

        for elem in content:
            paragraph = elem.get("paragraph")
            if paragraph:
                elements = paragraph.get("elements")
                for element in elements:
                    text_run = element.get("textRun")
                    if text_run:
                        link = text_run.get("textStyle", {}).get("link", {}).get("url")
                        if link:
                            links.append(link)

        return links
    except Exception as e:
        print(e)
        return "", []
