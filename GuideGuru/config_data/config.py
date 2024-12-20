import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

LOCAL_ENV = os.getenv("LOCAL_ENV")
BOT_TOKEN = os.getenv("BOT_TOKEN")
USERKEY_TEXT_RU = os.getenv("USERKEY_TEXT_RU")
USERKEY_CONTENT_WATCH = os.getenv("USERKEY_CONTENT_WATCH")
TURGENEV_API_KEY = os.getenv("TURGENEV_API_KEY")
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("eldo", "Правила для Эльдорадо"),
    ("mvideo", "Правила для Мвидео"),
    ("free_texts", "Свободные брифы"),
    ("check", "Проверить текст на стоп-слова"),
    ("unique", "Проверить текст на уникальность в text.ru"),
    ("content_watch", "Проверить текст на уникальность в content_watch.ru"),
    ("turgenev", "Проверить текст на Turgenev"),
    ("receipt", "Загрузить чек за гонорары"),
    ("history", "Все тексты за этот месяц"),
    ("last_month", "Все тексты за прошлый месяц"),
    ("all_texts", "Все тексты с ноября 2023 года"),
    ("vacation", "В отпуск или из отпуска"),
)
