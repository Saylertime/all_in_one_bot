import sqlite3


def connect_to_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    return conn, cursor

def close_db_connection(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()

def create_db():
    conn, cursor = connect_to_db()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        user_id INTEGER UNIQUE NOT NULL
                    )''')
    close_db_connection(conn, cursor)

def new_user(username, user_id):
    conn, cursor = connect_to_db()
    create_db()
    cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
    existing_user = cursor.fetchone()
    if existing_user or username == 'guide_guru_bot':
        return
    else:
        cursor.execute('''INSERT INTO users (username, user_id) VALUES (?, ?)''', (username, user_id))
    close_db_connection(conn, cursor)

def all_users_from_db():
    conn, cursor = connect_to_db()
    cursor.execute('''SELECT username, user_id FROM users''')
    all = cursor.fetchall()
    all_users = [i[0] for i in all]
    all_ids = [i[1] for i in all]
    close_db_connection(conn, cursor)
    print(all_users, all_ids)
    return all_users, all_ids

all_users_from_db()