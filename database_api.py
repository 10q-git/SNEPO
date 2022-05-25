import sqlite3


def create_database():
    try:
        sqlite_connection = sqlite3.connect('sqlite_urls.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("""CREATE TABLE urls(
                                    url TEXT NOT NULL UNIQUE,
                                    visited BOOLEAN NOT NULL);""")
        cursor.execute("""CREATE TABLE emails(
                                    email TEXT UNIQUE,
                                    url TEXT NOT NULL);""")
        cursor.execute("""CREATE TABLE names(
                                            name TEXT UNIQUE,
                                            url TEXT NOT NULL);""")
        cursor.execute("""CREATE TABLE phones(
                                            phone TEXT UNIQUE,
                                            url TEXT NOT NULL);""")
        cursor.execute("""CREATE TABLE file_urls(
                                             file_url TEXT NOT NULL UNIQUE);""")
        print("База данных подключена к SQLite")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            return sqlite_connection


def close_database(sqlite_connection):
    sqlite_connection.close()


def add_url_row(sqlite_connection, url):
    cursor = sqlite_connection.cursor()
    cursor.execute(f"""INSERT OR IGNORE INTO urls
                                            (url, visited)
                                            VALUES
                                            ('{url}', 0);""")
    cursor.close()


def get_not_visited_urls(sqlite_connection):
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT url 
                      FROM urls 
                      WHERE visited = 0;""")
    not_visited_urls = cursor.fetchall()
    cursor.close()
    return not_visited_urls

def mark_url(sqlite_connection, not_visited_url):
    cursor = sqlite_connection.cursor()
    cursor.execute(f"""UPDATE urls 
                       SET visited = 1 
                       WHERE url == '{not_visited_url}';""")
    sqlite_connection.commit()
    cursor.close()

def add_email(sqlite_connection, email, url):
    cursor = sqlite_connection.cursor()
    cursor.execute(f'''INSERT OR IGNORE INTO emails (email, url) VALUES ("{email}", "{url}");''')
    cursor.close()
    sqlite_connection.commit()


def add_names(sqlite_connection, name, url):
    cursor = sqlite_connection.cursor()
    cursor.execute(f'''INSERT OR IGNORE INTO names (name, url) VALUES ("{name}", "{url}");''')
    cursor.close()
    sqlite_connection.commit()


def add_phones(sqlite_connection, phone, url):
    cursor = sqlite_connection.cursor()
    cursor.execute(f'''INSERT OR IGNORE INTO phones (phone, url) VALUES ("{phone}", "{url}");''')
    cursor.close()
    sqlite_connection.commit()


def add_file_url(sqlite_connection, file_url):
    cursor = sqlite_connection.cursor()
    cursor.execute(f'''INSERT OR IGNORE INTO file_urls (file_url) VALUES ("{file_url}");''')
    cursor.close()
    sqlite_connection.commit()


def get_urls(sqlite_connection):
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT url 
                          FROM urls;""")
    fetched_urls = cursor.fetchall()
    urls = set()
    for url in fetched_urls:
        urls.add(url[0])
    return urls


def get_file_urls(sqlite_connection):
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT file_url 
                          FROM file_urls;""")
    fetched_file_urls = cursor.fetchall()
    file_urls = set()
    for file_url in fetched_file_urls:
        file_urls.add(file_url[0])
    return file_urls


def get_emails(sqlite_connection):
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT email 
                      FROM emails;""")
    fetched_emails = cursor.fetchall()
    emails = set()
    for email in fetched_emails:
        emails.add(email[0])
    return emails


def get_names(sqlite_connection):
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT name 
                      FROM names;""")
    fetched_names = cursor.fetchall()
    names = set()
    for name in fetched_names:
        names.add(name[0])
    return names


def get_phones(sqlite_connection):
    cursor = sqlite_connection.cursor()
    cursor.execute("""SELECT phone 
                      FROM phones;""")
    fetched_phones = cursor.fetchall()
    phones = set()
    for phone in fetched_phones:
        phones.add(phone[0])
    return phones
