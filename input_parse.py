import argparse

def createParser():
    parser = argparse.ArgumentParser(
        prog='SNEPO',
        description='Анализатор HTML-страниц',
        epilog='Author - 10q'
    )
    subparser = parser.add_subparsers()

    web_parser = subparser.add_parser('web_data', help='Collecting web site data')
    web_parser.add_argument('-u', '--url', required=True, type=str, help='Start page for analyse')
    web_parser.add_argument('-q', '--quick', action='store_true', default=False, help='Turn off saving file links')
    web_parser.add_argument('-s', '--structure', action='store_true', default=False, help='Create structure of WebApp')
    web_parser.add_argument('-n', '--names', action='store_true', default=False, help='Collect names')
    web_parser.add_argument('-e', '--email', action='store_true', default=False, help='Collect email addresses')
    web_parser.add_argument('-p', '--phone', action='store_true', default=False, help='Collect phone numbers')
    web_parser.add_argument('-o', '--fileOutput', action='store_true', default=False, help='Output to json file')

    meta_parser = subparser.add_parser('meta_data', help='Collecting file meta data')
    meta_parser.add_argument('-f', '--fileUrl', required=True, type=str, help='File url')
    meta_parser.add_argument('-o', '--fileOutput', action='store_true', default=False, help='Output to json file')

    return parser

#required=True,