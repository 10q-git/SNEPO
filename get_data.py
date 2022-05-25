from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import requests
import search_names
import search_phones
import search_emails
import database_api

# Инициализация переменных
int_url = set()
file_struct = dict()
names = set()
email_addresses = set()
phone_numbers = set()
visited_site = 0
running = True


# Проверка на валидность url
def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# Обход страницы и сбор данных
def collect_data_from_website(url, flags, sqlite_connection):
    global int_url, file_struct, names, email_addresses, phone_numbers

    urls = set()
    # Извлекаем домен
    domain_name = urlparse(url).netloc

    # Подготовка сессии для работы со страницей
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    # Установка user агента
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Запрос html кода
    html_content = session.get(url, headers=headers).content

    # Начло парсинга
    soup = BeautifulSoup(html_content, "lxml", from_encoding="UTF-8")

    # Перебираем тэги <a> в html коде
    for a_tag in soup.findAll("a"):
        # Сохраняем найденныю ссылку
        href = a_tag.attrs.get("href")

        # Проверяем на непустоту тэга <a>
        if href == "" or href is None:
            continue

        # Создаем ссылку на страницу
        if href not in url:
            href = urljoin(url, href)

        # Парсим ссылку
        parsed_href = urlparse(href)
        if "http" in parsed_href.scheme:
            # Обрезаем ненужное из ссылки
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            # Проверяем валидность
            if not valid_url(href):
                continue

            # Проверяем внутренняя ли ссылка, если нет, то пропускаем
            if domain_name not in href:
                continue

            # Отссеваем файлы для дальнейшего просмотра
            if not re.search(r'\.[a-zA-Z0-9]+$', href):
                urls.add(href)
            elif flags & 32 != 32:
                database_api.add_file_url(sqlite_connection, href)

    # Сбор ФИО
    if flags & 8:
        try:
            html_content.decode('UTF-8')
        except BaseException:
            names = names
        else:
            names = search_names.search(html_content.decode('UTF-8'))
            for name in names:
                database_api.add_names(sqlite_connection, name, url)
    # Сбор Emailов
    if flags & 4:
        try:
            html_content.decode('UTF-8')
        except BaseException:
            email_addresses = email_addresses
        else:
            email_addresses = search_emails.search(html_content.decode('UTF-8'))
            for email_address in email_addresses:
                database_api.add_email(sqlite_connection, email_address, url)
    # Сбор телефонных номеров
    if flags & 2:
        try:
            html_content.decode('UTF-8')
        except BaseException:
            phone_numbers = phone_numbers
        else:
            phone_numbers = search_phones.search(html_content.decode('UTF-8'))
            for phone_number in phone_numbers:
                database_api.add_phones(sqlite_connection, phone_number, url)

    return urls


# Паук
def crawl(url, flags, sqlite_connection):
    global visited_site, running
    if running:
        try:
            visited_site += 1
            # Сбор ссылок для дальнейшего обхода
            urls = collect_data_from_website(url, flags, sqlite_connection)
            for url in urls:
                database_api.add_url_row(sqlite_connection, url)

            not_visited_urls = database_api.get_not_visited_urls(sqlite_connection)

            for not_visited_url in not_visited_urls:
                if visited_site <= 100:
                    database_api.mark_url(sqlite_connection, str(not_visited_url[0]))
                    print(f"[*] Next link: {not_visited_url[0]}")
                    crawl(str(not_visited_url[0]), flags, sqlite_connection)
        except KeyboardInterrupt:
            print("Stoping...")
            exit()
