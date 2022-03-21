import pprint

def web_data_file_print(file_struct, names, email_addresses, phone_numbers):
    return

def web_data_console_print(file_struct, names, email_addresses, phone_numbers):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(file_struct)
    pp.pprint(names)
    pp.pprint(email_addresses)
    pp.pprint(phone_numbers)

def meta_data_console_print(meta_dict):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(meta_dict)

def meta_data_file_print(meta_dict):
    return

