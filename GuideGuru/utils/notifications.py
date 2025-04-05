from loader import bot
from utils.sheets import deadlines
from psql_maker import find_authors_id
from collections import defaultdict
from datetime import datetime
from pytz import timezone


async def deadlines_today():
    print("🔔 Функция deadlines_today() запущена!")
    print("Текущее время на сервере:", datetime.now())
    print("Текущее время по Москве:", datetime.now(timezone("Europe/Moscow")))
    authors_with_deadlines = await deadlines()
    authors_in_tg = defaultdict(str)
    for name_in_db, brief in authors_with_deadlines.items():
        print(name_in_db)
        telegram_id = await find_authors_id(name_in_db)
        if telegram_id:
            authors_in_tg[telegram_id] = brief

    try:
        for author_id, brief in authors_in_tg.items():
            print(author_id, brief)
            text_msg = "<b>НАПОМИНАЛКА</b>: у тебя сегодня дедлайн:\n\n" + "\n— ".join(
                brief
            )
            await bot.send_message(
                chat_id=author_id, text=text_msg, disable_web_page_preview=True
            )
    except Exception as e:
        print(e)
