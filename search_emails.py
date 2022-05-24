import re

def search(html_content):
    emails = set(re.findall(r'[_a-zA-Z0-9\-\+]+(?:\.[_a-zA-Z0-9\-]+)*@[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*(?:\.[a-zA-Z]{2,})', html_content))
    return emails
