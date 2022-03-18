import re

def search(html_content):
    emails = set(re.findall(r'[_a-z0-9\-\+]+(?:\.[_a-z0-9\-]+)*@[a-z0-9\-]+(?:\.[a-z0-9\-]+)*(?:\.[a-z]{2,})', html_content))
    return emails
