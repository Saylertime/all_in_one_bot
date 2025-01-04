import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from config_data import config
from handlers import routers
from loader import bot, dp
from middlewares.logging_middleware import LoggingMiddleware
from utils.logger import logger

LOCAL_ENV = config.LOCAL_ENV
BASE_URL = "https://glinkin.pro"
WEBHOOK_PATH = "/webhook_report"
PORT = 5003
HOST = "0.0.0.0"


# Функция для установки командного меню для бота
async def set_commands():
    commands = [
        BotCommand(command=cmd, description=desc)
        for cmd, desc in config.DEFAULT_COMMANDS
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


# Функция, которая будет вызвана при запуске бота
async def on_startup() -> None:
    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    await bot.send_message(chat_id=68086662, text="Бот запущен на вебхуках!")


# Функция, которая будет вызвана при остановке бота
async def on_shutdown() -> None:
    await bot.send_message(chat_id=68086662, text="Бот остановлен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


# Middleware для подавления BadStatusLine
@web.middleware
async def suppress_bad_status_line(request, handler):
    try:
        return await handler(request)
    except BadStatusLine:
        logger.warning("BadStatusLine exception suppressed.")
        return web.Response(status=400, text="Bad request")


# Основная функция, которая запускает приложение
def main_webhook() -> None:
    for router in routers:
        dp.include_router(router)

    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application(middlewares=[suppress_bad_status_line])
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=HOST, port=PORT)


async def main():
    await set_commands()
    for router in routers:
        dp.include_router(router)

    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if LOCAL_ENV == "local":
        asyncio.run(main())
    else:
        main_webhook()
