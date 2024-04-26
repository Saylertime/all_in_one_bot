import os
# import openai
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

LOCAL_ENV = os.getenv("LOCAL_ENV")
BOT_TOKEN = os.getenv("BOT_TOKEN")
openai_api_key = os.getenv("CHATGPT_API_KEY")
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
USERKEY_TEXT_RU = os.getenv("USERKEY_TEXT_RU")


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("authors", "Все авторы"),
    ("free_authors", "Свободные авторы"),
    ("free_texts", "Свободные брифы"),
    ("deadlines", "Дедлайны"),
    ("notification", "Напоминалка"),
    ("new_author", "Добавить автора"),
    ("money", "Гонорары за месяц"),
    ("stats_month", "Статистика по текстам за месяц"),
    ("history", "Инфа по отдельному автору"),
    ("all_texts", "Тексты автора за всё время"),
    ("test", "test"),
)
