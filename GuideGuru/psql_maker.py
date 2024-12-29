from config_data import config
import asyncpg

dbname = config.DB_NAME
user = config.DB_USER
password = config.DB_PASSWORD
host = config.DB_HOST


async def connect_to_db():
    """Создаёт асинхронное подключение к базе данных."""
    conn = await asyncpg.connect(
        database=dbname, user=user, password=password, host=host
    )
    return conn


async def close_db_connection(conn):
    """Закрывает асинхронное подключение к базе данных."""
    await conn.close()


async def all_authors():
    """Возвращает список всех авторов."""
    conn = await connect_to_db()
    try:
        sql = "SELECT name, nickname, name_in_db FROM public.authors"
        authors = await conn.fetch(sql)
        return authors
    finally:
        await conn.close()


async def find_author(nickname):
    conn = await connect_to_db()
    try:
        sql = f"SELECT name_in_db FROM public.authors WHERE nickname = '{nickname}'"
        record = await conn.fetchrow(sql)
        if record:
            return record["name_in_db"]
        return None
    finally:
        await conn.close()


async def author_on_vacation(nickname):
    conn = await connect_to_db()
    try:
        sql = f"SELECT vacation FROM public.authors WHERE nickname = '@{nickname}';"
        vacation = await conn.fetch(sql)
        return vacation
    finally:
        await conn.close()


async def update_vacation_status(nickname, status):
    conn = await connect_to_db()
    try:
        sql = """UPDATE public.authors 
                 SET vacation = $1 
                 WHERE nickname = $2;"""
        await conn.execute(sql, status, f"@{nickname}")
    finally:
        await conn.close()


async def new_table_stop_words():
    conn = await connect_to_db()
    try:
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
    finally:
        await conn.close()


async def select_word_from_stop_words(word):
    conn = await connect_to_db()
    try:
        sql = f"SELECT word FROM words WHERE word=$1;"
        result = await conn.fetchrow(sql, word)
        return result["word"] if result else None
    finally:
        await conn.close()


async def insert_new_word(word):
    conn = await connect_to_db()
    try:
        word_in_bd = await select_word_from_stop_words(word)
        print(word_in_bd)
        if not word_in_bd:
            sql = "INSERT INTO words (word) VALUES ($1);"
            await conn.execute(sql, word)
            return f'Слово "{word}" добавлено в базу стоп-слов'
        else:
            return f'Слово "{word}" уже есть в базе'
    finally:
        await conn.close()


async def delete_stop_word(word):
    conn = await connect_to_db()
    try:
        if await select_word_from_stop_words(word):
            sql = "DELETE FROM words WHERE word=$1"
            await conn.execute(sql, word)
            return f'Слово "{word}" удалено из базы стоп-слов'
        else:
            return f'Слова "{word}" нет в базе'
    finally:
        await conn.close()


async def all_stop_words():
    conn = await connect_to_db()
    try:
        sql = "SELECT word FROM words;"
        rows = await conn.fetch(sql)
        words = [row[0] for row in rows]
        return words
    finally:
        await conn.close()
