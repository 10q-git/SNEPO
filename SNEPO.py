import create_file_struct
import get_data
import get_meta_data
import input_parse
import logo
import output

if __name__ == "__main__":
    logo.logo_print()

    parser = input_parse.createParser()
    parser.print_help()

    input_list = input("\nLets try:\n").split()
    namespace = parser.parse_args(input_list)
    print(namespace)

    if 'url' in namespace:
        url = namespace.url

        flags = 0
        if namespace.structure:
            flags = flags | 16
        if namespace.names:
            flags = flags | 8
        if namespace.email:
            flags = flags | 4
        if namespace.phone:
            flags = flags | 2
        if namespace.fileOutput:
            flags = flags | 1

        int_url, file_struct, names, email_addresses, phone_numbers = get_data.crawl(url, flags)

        file_struct = dict()
        if flags & 16:
            file_struct = create_file_struct.create(int_url)

        if flags & 1:
            output.web_data_file_print(file_struct, names, email_addresses, phone_numbers)
        else:
            output.web_data_console_print(file_struct, names, email_addresses, phone_numbers)

    elif 'fileUrl' in namespace:
        meta_dict = get_meta_data.get(namespace.fileUrl)

        if namespace.fileOutput:
            output.meta_data_file_print(meta_dict)
        else:
            output.meta_data_console_print(meta_dict)

    #print("[+] Total Internal links:", len(int_url))

