import pprint

def file_print(file_struct, names, email_addresses, phone_numbers):
    return

def console_print(file_struct, names, email_addresses, phone_numbers):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(file_struct)
    pp.pprint(names)
    pp.pprint(email_addresses)
    pp.pprint(phone_numbers)
