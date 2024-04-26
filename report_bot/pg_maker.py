from config_data import config
from datetime import datetime
from utils.calendar import current_day
import psycopg2
import pytz

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

def add_author(name, nickname, name_in_db, about='', phone=''):
    conn, cursor = connect_to_db()
    sql = f"INSERT INTO public.authors (name, nickname, name_in_db, about, phone) " \
          f"VALUES ('{name}', '{nickname}', '{name_in_db}', '{about}', '{phone}')"
    cursor.execute(sql)
    print(f"{nickname} добавлен")
    close_db_connection(conn, cursor)

def delete_author(name_in_db):
    conn, cursor = connect_to_db()
    sql = f"""DELETE from public.authors WHERE name_in_db=%s"""
    cursor.execute(sql, (name_in_db, ))
    close_db_connection(conn, cursor)
    return cursor.rowcount

def all_authors():
    conn, cursor = connect_to_db()
    sql = "SELECT name, nickname, name_in_db FROM public.authors"
    cursor.execute(sql)
    authors = cursor.fetchall()
    close_db_connection(conn, cursor)
    return authors

def create_db():
    conn, cursor = connect_to_db()
    sql = 'CREATE TABLE IF NOT EXISTS public.authors (name VARCHAR, nickname VARCHAR, name_in_db VARCHAR, phone VARCHAR, about VARCHAR);'
    cursor.execute(sql)
    close_db_connection(conn, cursor)

def refresh_db():
    conn, cursor = connect_to_db()
    try:
        cursor.execute("DROP TABLE public.authors;")
    except:
        pass
    create_db()
    insert_data_sql = """
        INSERT INTO public.authors (name, nickname, name_in_db)
        VALUES (%s, %s, %s)
    """

    authors_data = [
        ('Кирилл Мироненко', '@quir1ll', 'Кирилл'),
        ('Кирилл Моралес', '@kirill_morales', 'Моралес'),
        ('Саша Никитенко', '@isaywheee', 'Саша'),
        ('Артем Вайс', '@Vice_Mallow', 'Артем'),
        ('Екатерина Генералова', '@Catygen', 'Генералова'),
        ('Дина Скворцова', '@interneuronic', 'Дина'),
        ('Егор Бабин', '@baego', 'Егор'),
        ('Арсений Мирный', '@ArseniyMirniy', 'Арсений'),
        ('Вадим Макаренко', '@Mkarow', 'Вадим'),
        ('Ирина Гродзинская', '@Irina_Grodzinskaya', 'Ира'),
        ('Анна Османова', '@annacalico', 'Анна'),
        ('Шамиль Алиуллов', '@aliullov_sh', 'Шамиль'),
        ('Ана Бартенева', '@the_barteneva', 'Ана'),
        ('Борис Стародубцев', '@johnyscreams', 'Бо'),
        ('Вика Баранова', '@barvikki', 'Вика'),
        ('Сергей Рыбалко', '@pescadotravel', 'Сергей'),
        ('Алина Орлова', '@suspicious_fox', 'Алина'),
        ('Фил Кучканов', '@kuchkanov', 'Фил'),
        ('Ксения Седна', '@Sedn04ka', 'Седна'),
        ('Никита Баранов', '@Hurtson', 'Никита'),
        ('Дмитрий Корниенко', '@dimkor42', 'Дима'),
        ('Дарья Роман', '@drrmmn', 'Дарья'),
        ('Роман Шумялов', '@marabouto', 'Рома'),
        ('Ксения Бурыгина', '@vegur', 'Ксения'),
    ]
    cursor.executemany(insert_data_sql, authors_data)
    close_db_connection(conn, cursor)

def find_author(name):
    conn, cursor = connect_to_db()
    sql = f"SELECT nickname FROM public.authors WHERE name_in_db = '{name}'"
    cursor.execute(sql)
    author = cursor.fetchone()
    close_db_connection(conn, cursor)
    return author

def drop_table(table_name):
    conn, cursor = connect_to_db()
    sql = f"""DROP TABLE IF EXISTS {table_name};"""
    cursor.execute(sql)
    close_db_connection(conn, cursor)

def new_table():
    conn, cursor = connect_to_db()
    sql = """CREATE TABLE IF NOT EXISTS public.notifications 
    (
    user_id INTEGER, 
    n_date VARCHAR, 
    n_time VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    text VARCHAR, 
    is_sent BOOL DEFAULT FALSE
    );
    """
    cursor.execute(sql)
    close_db_connection(conn, cursor)

def new_notifications(user_id, n_date, n_time, text):
    conn, cursor = connect_to_db()
    sql = """INSERT INTO public.notifications 
    (
    user_id, 
    n_date, 
    n_time, 
    text
    )
    VALUES (%s, %s, %s::TIME, %s)"""
    values = (user_id, n_date, n_time, text)
    cursor.execute(sql, values)
    close_db_connection(conn, cursor)

def find_notifications(user_id):
    conn, cursor = connect_to_db()
    sql = f"SELECT * FROM public.notifications WHERE user_id={user_id}"
    cursor.execute(sql)
    notifications = cursor.fetchall()
    close_db_connection(conn, cursor)
    return notifications

def find_for_tasks():
    new_table()
    desired_timezone = pytz.timezone('Europe/Moscow')
    today, tomorrow = current_day()
    conn, cursor = connect_to_db()
    sql = """
        SELECT user_id, n_time, text
        FROM public.notifications
        WHERE is_sent=False 
        AND n_date=%s
        AND n_time=%s;
        """
    current_time = datetime.now(desired_timezone).replace(second=0).strftime("%H:%M:%S")
    cursor.execute(sql, (today, current_time))
    notifications = cursor.fetchall()
    close_db_connection(conn, cursor)
    return notifications
