from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
#from threading import Thread
#from multiprocessing import Process
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
import requests
import search_names
import search_phones
import search_emails
import logging

#Инициализация переменных
int_url = set()
file_struct = dict()
names = set()
email_addresses = set()
phone_numbers = set()
visited_site = 0

#Проверка на валидность url
def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#Обход страницы и сбор данных
def collect_data_from_website(url, flags):
    global int_url, file_struct, names, email_addresses, phone_numbers

    urls = set()
    #Извлекаем домен
    domain_name = urlparse(url).netloc

    #Подготовка сессии для работы со страницей
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    #Установка user агента
    headers = {'User-Agent': 'Mozilla/5.0'}

    #Запрос html кода
    html_content = session.get(url, headers=headers).content

    #Начло парсинга
    soup = BeautifulSoup(html_content, "lxml", from_encoding="UTF-8")

    #Перебираем тэги <a> в html коде
    for a_tag in soup.findAll("a"):
        #Сохраняем найденныю ссылку
        href = a_tag.attrs.get("href")

        #Проверяем на непустоту тэга <a>
        if href == "" or href is None:
            continue

        #Создаем ссылку на страницу
        if href not in url:
            href = urljoin(url, href)

        #Парсим ссылку
        parsed_href = urlparse(href)
        if "http" in parsed_href.scheme:
            #Обрезаем ненужное из ссылки
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            #Проверяем валидность
            if not valid_url(href):
                continue

            #Проверяем есть ли такая ссылка в наборе
            if href in int_url:
                continue

            #Проверяем внутренняя ли ссылка, если нет, то пропускаем
            if domain_name not in href:
                continue
            print(f"[*] Internal link: {href}")

            int_url.add(href)
            #Отссеваем файлы для дальнейшего просмотра
            if not re.search(r'\.[a-zA-Z]+$', href):
                urls.add(href)

    #Сбор ФИО
    if flags & 8:
        try:
            html_content.decode('UTF-8')
        except BaseException:
            names = names
        else:
            names = names.union(search_names.search(html_content.decode('UTF-8')))
    #Сбор Emailов
    if flags & 4:
        try:
            html_content.decode('UTF-8')
        except BaseException:
            email_addresses = email_addresses
        else:
            email_addresses = email_addresses.union(search_emails.search(html_content.decode('UTF-8')))
    #Сбор телефонных номеров
    if flags & 2:
        try:
            html_content.decode('UTF-8')
        except BaseException:
            phone_numbers = phone_numbers
        else:
            phone_numbers = phone_numbers.union(search_phones.search(html_content.decode('UTF-8')))
    return urls

#Паук
def crawl(url, flags, num = 0):
    global visited_site
    visited_site += 1
    #Сбор ссылок для дальнейшего обхода
    links = collect_data_from_website(url, flags)
    #if visited_site < 1:
    #Обход найденных ссылок
    for link in links:
      crawl(link, flags)
    return int_url, file_struct, names, email_addresses, phone_numbers
