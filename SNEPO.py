import FileStruct
import get_data
import pprint
import input_parse
import logo
import output

if __name__ == "__main__":
    logo.logo_print()

    parser = input_parse.createParser()
    parser.print_help()

    input = input("\nLets try:\n").split()
    namespace = parser.parse_args(input)
    print(namespace)

    url = namespace.url

    flags = 0
    if namespace.structure:
        flags = flags | 32
    if namespace.names:
        flags = flags | 16
    if namespace.email:
        flags = flags | 8
    if namespace.phone:
        flags = flags | 4
    if namespace.filePath:
        flags = flags | 2
    if namespace.fileOutput:
        flags = flags | 1

    int_url, file_struct, names, email_addresses, phone_numbers = get_data.crawl(url, flags)

    if flags & 32:
        file_struct = FileStruct.create_file_struct(int_url)

    if flags & 1:
        output.file_print(file_struct, names, email_addresses, phone_numbers)
    else:
        output.console_print(file_struct, names, email_addresses, phone_numbers)

    print("[+] Total Internal links:", len(int_url))

