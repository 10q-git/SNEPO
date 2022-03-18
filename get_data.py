from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from threading import Thread
from multiprocessing import Process
import requests
import search_names
import search_phones
import search_emails

int_url = set()
file_struct = dict()
names = set()
email_addresses = set()
phone_numbers = set()
procs = []


def valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def website_links(url, flags):
    global int_url, file_struct, names, email_addresses, phone_numbers

    urls = set()
    # извлекаем доменное имя из URL
    domain_name = urlparse(url).netloc
    html_content = requests.get(url).content
    soup = BeautifulSoup(html_content, "lxml", from_encoding="UTF-8")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            continue
        if href not in url:
            href = urljoin(url, href)
        parsed_href = urlparse(href)
        # удалить параметры URL GET, фрагменты URL и т. д.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not valid_url(href):
            # недействительный URL
            continue
        if href in int_url:
            # уже в наборе
            continue
        if domain_name not in href:
            continue
        print(f"[*] Internal link: {href}")
        urls.add(href)
        int_url.add(href)

    if flags & 16:
        names = names.union(search_names.search(html_content.decode('UTF-8')))
    if flags & 8:
        email_addresses = email_addresses.union(search_emails.search(html_content.decode('UTF-8')))
    if flags & 4:
        phone_numbers = phone_numbers.union(search_phones.search(html_content.decode('UTF-8')))

    return urls


def crawl(url, flags):
    global procs
    try:
        links = website_links(url, flags)
    except:
        links = set()

    for link in links:
        proc = Process(target=crawl, args=(link, flags))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    return int_url, file_struct, names, email_addresses, phone_numbers
