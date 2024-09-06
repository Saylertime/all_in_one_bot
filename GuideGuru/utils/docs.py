import os.path
from psql_maker import all_stop_words

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

creds = None

if os.path.exists("token2.json"):
    creds = Credentials.from_authorized_user_file("token2.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token2.json", "w") as token:
      token.write(creds.to_json())


def check_text(doc_id):
    stop_words = all_stop_words()

    try:
        service = build("docs", "v1", credentials=creds)

        document = service.documents().get(documentId=doc_id).execute()

        content = document.get("body").get("content")

        stop_count = 0
        e_count = 0
        words = []

        for elem in content:
            paragraph = elem.get("paragraph")
            if paragraph:
                elements = paragraph.get("elements")
                for element in elements:
                    text_run = element.get("textRun")
                    if text_run:
                        content = text_run.get("content")
                        if content:
                            all_content = content.split()
                            for word in all_content:
                                if word.lower() in stop_words:
                                    words.append(word)
                                    stop_count += 1
                                elif 'ё' in word.lower() or 'Ё' in word.lower():
                                    e_count += 1

        if stop_count == 0 and e_count == 0:
            msg = "Стоп-слов нет, ты молодчуля ;)"
        elif stop_count and e_count:
            msg = f"Стоп-слов в тексте: {stop_count}. Вот они, слева направо:\n\n"
            msg += ", ".join(words)
            msg += f"\n\nА еще убери буквы Ё. У тебя в тексте их {e_count}"
        elif e_count:
            msg = f"Убери буквы Ё из текста. У тебя их {e_count}"
        else:
            msg = f"Стоп-слов в тексте: {stop_count}. Вот они, слева направо:\n\n"
            msg += ", ".join(words)
        print(msg)
        return msg


    except HttpError as err:
        print(err)

def get_content(doc_id):
    try:
        service = build("docs", "v1", credentials=creds)

        document = service.documents().get(documentId=doc_id).execute()

        content = document.get("body").get("content")

        full_text = ""
        for elem in content:
            paragraph = elem.get("paragraph")
            if paragraph:
                elements = paragraph.get("elements")
                for element in elements:
                    text_run = element.get("textRun")
                    if text_run:
                        content = text_run.get("content").strip()
                        if content:
                            full_text += f" {content}"
        return full_text
    except Exception as e:
        print(e)
        return ''
