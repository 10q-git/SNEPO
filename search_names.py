import re

def search(html_content):
    names = set(re.findall(r'[А-ЯЁ][а-яё]*\.? *[А-ЯЁ][а-яё]*\.? *[А-ЯЁ][а-яё]+', html_content))
    names = names.union(set(re.findall(r'[А-ЯЁ][а-яё]+ *[А-ЯЁ][а-яё]*\.? *[А-ЯЁ][а-яё]*\.?', html_content)))
    return names

