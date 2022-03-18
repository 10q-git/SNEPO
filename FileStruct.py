from urllib.parse import urlparse

def add_path(file_struct, path):
    split_path = path.split('/')
    if split_path[len(split_path)-1] == "":
        split_path.pop(len(split_path)-1)

    if split_path:
        file = split_path[0]
        if file in file_struct.keys():
            split_path.pop(0)
            add_path(file_struct[file], '/'.join(split_path))
        else:
            file_struct[file] = dict()

def create_file_struct(int_url):
    file_struct = dict()
    for url in int_url:
        path = urlparse(url).path[1:]
        split_path = path.split("/")
        add_path(file_struct, path)

    return file_struct
