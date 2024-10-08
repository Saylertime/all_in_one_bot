from config_data import config
import psycopg2

dbname = config.DB_NAME
user = config.DB_USER
password = config.DB_PASSWORD
host = config.DB_HOST

def connect_to_db():
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cursor = conn.cursor()
    conn.autocommit = True
    return conn, cursor

def close_db_connection(conn, cursor):
    cursor.close()
    conn.close()

def all_authors():
    conn, cursor = connect_to_db()
    sql = "SELECT name, nickname, name_in_db FROM public.authors"
    cursor.execute(sql)
    authors = cursor.fetchall()
    close_db_connection(conn, cursor)
    return authors

def find_author(nickname):
    conn, cursor = connect_to_db()
    sql = f"SELECT name_in_db FROM public.authors WHERE nickname = '{nickname}'"
    cursor.execute(sql)
    author = cursor.fetchone()
    close_db_connection(conn, cursor)
    return author

def author_on_vacation(nickname):
    conn, cursor = connect_to_db()
    sql = f"SELECT vacation FROM public.authors WHERE nickname = '@{nickname}';"
    cursor.execute(sql)
    vacation = cursor.fetchone()
    close_db_connection(conn, cursor)
    return vacation

def update_vacation_status(nickname, status):
    conn, cursor = connect_to_db()
    sql = f"UPDATE public.authors SET vacation = {status} WHERE nickname = '@{nickname}';"
    cursor.execute(sql)
    close_db_connection(conn, cursor)


def new_table_stop_words():
    conn, cursor = connect_to_db()
    sql = """CREATE TABLE IF NOT EXISTS words (word VARCHAR);"""
    cursor.execute(sql)
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
    cursor.execute(insert_data_sql)
    close_db_connection(conn, cursor)

def select_word_from_stop_words(word):
    conn, cursor = connect_to_db()
    sql = f"SELECT word FROM words WHERE word=%s;"
    cursor.execute(sql, (word,))
    result = cursor.fetchone()
    return result

def insert_new_word(word):
    conn, cursor = connect_to_db()
    if not select_word_from_stop_words(word):
        sql = "INSERT INTO words (word) VALUES (%s);"
        cursor.execute(sql, (word,))
        return f'Слово "{word}" добавлено в базу стоп-слов'
    else:
        return f'Слово "{word}" уже есть в базе'
    close_db_connection(conn, cursor)

def delete_stop_word(word):
    conn, cursor = connect_to_db()
    if select_word_from_stop_words(word):
        sql = "DELETE FROM words WHERE word=%s"
        cursor.execute(sql, (word, ))
        return f'Слово "{word}" удалено из базы стоп-слов'
    else:
        return f'Слова "{word}" нет в базе'
    close_db_connection(conn, cursor)

def all_stop_words():
    conn, cursor = connect_to_db()
    cursor.execute("SELECT word FROM words;")
    rows = cursor.fetchall()
    words = [row[0] for row in rows]
    return words
