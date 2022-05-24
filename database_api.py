import sqlite3
def create_database():
    try:
        sqlite_connection = sqlite3.connect('sqlite_urls.db')
        sqlite_create_url_table = '''CREATE TABLE urls(
                                    url TEXT NOT NULL UNIQUE,
                                    visited BOOLEAN NOT NULL);'''
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_url_table)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            return sqlite_connection

def close_database(sqlite_connection):
    sqlite_connection.close()



