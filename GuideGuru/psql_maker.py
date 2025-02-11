from config_data import config
from contextlib import asynccontextmanager
import asyncpg

dbname = config.DB_NAME
user = config.DB_USER
password = config.DB_PASSWORD
host = config.DB_HOST


@asynccontextmanager
async def db_connection():
    """Контекстный менеджер для асинхронного подключения к базе данных."""
    conn = await asyncpg.connect(
        database=dbname, user=user, password=password, host=host
    )
    try:
        yield conn
    finally:
        await conn.close()


async def update_author_with_id(user_id, nickname):
    async with db_connection() as conn:
        sql = "UPDATE public.authors SET user_id = $1 WHERE nickname = $2 AND user_id is NULL"
        await conn.execute(sql, user_id, nickname)


async def all_authors():
    """Возвращает список всех авторов."""
    async with db_connection() as conn:
        sql = "SELECT name, nickname, name_in_db, user_id FROM public.authors"
        authors = await conn.fetch(sql)
        return authors


async def find_author(nickname):
    async with db_connection() as conn:
        sql = f"SELECT name_in_db FROM public.authors WHERE nickname = '{nickname}'"
        record = await conn.fetchrow(sql)
        if record:
            return record["name_in_db"]
        return None


async def author_on_vacation(nickname):
    async with db_connection() as conn:
        sql = f"SELECT vacation FROM public.authors WHERE nickname = '@{nickname}';"
        vacation = await conn.fetch(sql)
        return vacation


async def update_vacation_status(nickname, status):
    async with db_connection() as conn:
        sql = """UPDATE public.authors 
                 SET vacation = $1 
                 WHERE nickname = $2;"""
        await conn.execute(sql, status, f"@{nickname}")


async def new_table_stop_words():
    async with db_connection() as conn:
        sql = """CREATE TABLE IF NOT EXISTS words (word VARCHAR);"""
        await conn.execute(sql)
        insert_data_sql = """
            INSERT INTO words (word) VALUES
            ('данный'), ('данная'), ('данное'), ('данного'), ('данной'),
            ('является'), ('являются'), ('являющийся'), ('являющиеся'), ('являющаяся'), ('являющейся'), ('являлся'), ('являлась'), ('являться'),
            ('являлось'), ('являлись'), ('обладать'), ('обладаю'), ('обладаем'), ('обладаешь'), ('обладаете'), ('обладает'), ('обладают'),
            ('обладал'), ('обладала'), ('обладало'), ('обладали'), ('обладая'), ('обладав'), ('обладавши'), ('обладай'), ('обладайте'),
            ('обладающий'), ('обладающего'), ('обладающему'), ('обладающим'), ('обладающем'), ('обладающая'), ('обладающей'), ('обладающую'),
            ('обладающею'), ('обладающее'), ('обладающие'), ('обладающих'), ('обладающими'), ('обладавший'), ('обладавшего'), ('обладавшему'),
            ('обладавшим'), ('обладавшем'), ('обладавшая'), ('обладавшей'), ('обладавшую'), ('обладавшею'), ('обладавшее'), ('обладавшие'),
            ('обладавших'), ('обладавшими'), ('оснащен'), ('оснащена'), ('оснащено'), ('оснащенный'), ('оснащенная'), ('оснащенные'),
            ('оснащенное'), ('оснащён'), ('оснащённый'), ('оснащённая'), ('оснащённые'), ('оснащённое'),
            ('снабжен'), ('снабжена'), ('снабжено'), ('снабженный'), ('снабженная'), ('снабженные'), ('снабженное'),
            ('снабжён'), ('снабжённый'), ('снабжённая'), ('снабжённые'), ('снабжённое'), ('снабдил'), ('снабдила'), ('снабдили'), ('снабдило'),
            ('снабдят'), ('снабдит'),
            ('оборудован'), ('оборудована'), ('оборудовано'), ('оборудованный'), ('оборудованная'), ('оборудованные'), ('оборудованное'),
            ('оборудовали'), ('оборудовал'), ('оборудовала'), ('оборудуют'), ('оборудует'), ('оборудовать'), ('оборудованных'),
            ('осуществляется'), ('осуществляются'), ('осуществляемый'), ('осуществляемая'), ('осуществляет'), ('осуществляют'),
            ('осуществлял'), ('осуществляла'), ('осуществлять'),
            ('обеспечивает'), ('обеспечивают'), ('обеспечивающий'), ('обеспечивающая'), ('обеспечивающие'), ('обеспечивающее'), ('обеспечил'),
            ('обеспечила'), ('обеспечит'), ('обеспечат'), ('обеспечить'),
            ('гарантирует'), ('гарантируют'), ('гарантирующий'), ('гарантирующая'), ('гарантирующие');
        """
        await conn.execute(insert_data_sql)


async def select_word_from_stop_words(word):
    async with db_connection() as conn:
        sql = f"SELECT word FROM words WHERE word=$1;"
        result = await conn.fetchrow(sql, word)
        return result["word"] if result else None


async def insert_new_word(word):
    async with db_connection() as conn:
        word_in_bd = await select_word_from_stop_words(word)
        print(word_in_bd)
        if not word_in_bd:
            sql = "INSERT INTO words (word) VALUES ($1);"
            await conn.execute(sql, word)
            return f'Слово "{word}" добавлено в базу стоп-слов'
        else:
            return f'Слово "{word}" уже есть в базе'


async def delete_stop_word(word):
    async with db_connection() as conn:
        if await select_word_from_stop_words(word):
            sql = "DELETE FROM words WHERE word=$1"
            await conn.execute(sql, word)
            return f'Слово "{word}" удалено из базы стоп-слов'
        else:
            return f'Слова "{word}" нет в базе'


async def all_stop_words():
    async with db_connection() as conn:
        sql = "SELECT word FROM words;"
        rows = await conn.fetch(sql)
        words = [row[0] for row in rows]
        return words
