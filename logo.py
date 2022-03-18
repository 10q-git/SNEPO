import pprint

def logo_print():
    file = open("logo", "r")
    lines = file.readlines()

    for line in lines:
        print("\033[3m\033[31m{}\033[0m".format(line[1:-1]))

    for i in range(2):
        print("\n")



