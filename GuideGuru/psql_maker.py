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
