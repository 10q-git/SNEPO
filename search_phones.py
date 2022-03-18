import re

def search(html_content):
    names = (re.findall(r'(?:(?:8|\+7)[\- ]?)\(?\d{3,4}\)?[\- ]?\d{2,3}[\- ]?\d{2}[\- ]?\d{2}', html_content))
    return names

