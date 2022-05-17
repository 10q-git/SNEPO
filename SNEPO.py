import os

import create_file_struct
import get_data
import get_meta_data
import input_parse
import logo
import output
import logging

if __name__ == "__main__":
    logging.basicConfig(filename="log.txt", level=logging.INFO)
    #Вывод лого
    logo.logo_print()

    #Создание парсера и вывод помощи
    parser = input_parse.createParser()
    parser.print_help()

    #Ввод входной строки и парсинг аргументов
    input_list = input("\nLets try:\n").split()
    namespace = parser.parse_args(input_list)

    ##print(namespace)

    #Если запущен мод web_data
    if 'url' in namespace:
        #Сохранение исходного url
        url = namespace.url

        #Создание переменной содержащей флаги
        flags = 0
        #Флаг структуры
        if namespace.structure:
            flags = flags | 16
        #Флаг ФИО
        if namespace.names:
            flags = flags | 8
        #Флаг Emailов
        if namespace.email:
            flags = flags | 4
        #Флаг номеров телефонов
        if namespace.phone:
            flags = flags | 2
        #Флаг вывода в файл
        if namespace.fileOutput:
            flags = flags | 1

        #Сбор данных
        int_url, file_struct, names, email_addresses, phone_numbers = get_data.crawl(url, flags)

        #Воссоздание файловой структуры
        file_struct = dict()
        if flags & 16:
            file_struct = create_file_struct.create(int_url)

        #Вывод результатов
        if flags & 1:
            output.web_data_file_print(file_struct, names, email_addresses, phone_numbers)
        else:
            output.web_data_console_print(file_struct, names, email_addresses, phone_numbers)

    #Если запущен мод meta_data
    elif 'fileUrl' in namespace:
        #Сбор метаданных
        meta_dict = get_meta_data.get(namespace.fileUrl)
        #Очистка временных файлов
        os.system("rm -r tmp")

        #Вывод результата
        if namespace.fileOutput:
            output.meta_data_file_print(meta_dict)
        else:
            output.meta_data_console_print(meta_dict)

    #print("[+] Total Internal links:", len(int_url))

