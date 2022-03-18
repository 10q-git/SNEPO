import re

def search(html_content):
    names = set(re.findall(r'[А-Я,Ё][а-я,ё]*\.? *[А-Я,Ё][а-я,ё]*\.? *[А-Я,Ё][а-я,ё]+', html_content))
    names = names.union(set(re.findall(r'[А-Я,Ё][а-я,ё]+ *[А-Я,Ё][а-я,ё]*\.? *[А-Я,Ё][а-я,ё]*\.?', html_content)))
    return names

