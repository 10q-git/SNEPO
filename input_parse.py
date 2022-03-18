import argparse

def createParser():
    parser = argparse.ArgumentParser(
        prog='SNEPO',
        description='Анализатор HTML-страниц',
        epilog='Author - 10q'
    )
    parser.add_argument('-u', '--url', required=True, type=str, help='Start page for analyse')
    parser.add_argument('-s', '--structure', action='store_true', default=False, help='Create structure of WebApp')
    parser.add_argument('-n', '--names', action='store_true', default=False, help='Collect names')
    parser.add_argument('-e', '--email', action='store_true', default=False, help='Collect email addresses')
    parser.add_argument('-p', '--phone', action='store_true', default=False, help='Collect phone numbers')
    parser.add_argument('-f', '--filePath', type=str, help='Try to take metadata from file')
    parser.add_argument('-o', '--fileOutput', action='store_true', default=False, help='Output to json file')

    return parser
