import pprint
import json

def web_data_file_print(file_struct, names, email_addresses, phone_numbers):
    file_struct_json = json.dumps(file_struct) + "\n"
    names_json = json.dumps(list(names)) + "\n"
    email_addresses_json = json.dumps(list(email_addresses)) + "\n"
    phone_numbers_json = json.dumps(list(phone_numbers)) + "\n"

    output_file = open('web_data.json', 'w')
    output_file.write(file_struct_json)
    output_file.write(names_json)
    output_file.write(email_addresses_json)
    output_file.write(phone_numbers_json)

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
    meta_data_json = json.dumps(meta_dict)
    output_file = open('web_data.json', 'w')
    output_file.write(meta_data_json)

