import requests
import zipfile
import xml.etree.ElementTree as ET
from PIL import Image
from PIL.ExifTags import TAGS


def get_from_office_x(file_name):
    zip_obj = zipfile.ZipFile(file_name)
    zip_obj.extractall('./tmp/unziped')
    zip_obj.close()

    meta_data = dict()
    tree = ET.parse(f'./tmp/unziped/docProps/core.xml')
    root = tree.getroot()
    for child in root:
        meta_data[child.tag.split('}')[-1]] = child.text

    return meta_data

def get_exif_data(file_name):
    ret = {}
    i = Image.open(file_name)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

def get(url):
    file_name = url.split('/')[-1]
    file = open(f'./tmp/{file_name}', "wb")
    ufr = requests.get(url)
    file.write(ufr.content)
    file.close

    meta_data = dict()
    file_format = file_name.split('.')[-1]
    file_format = str.lower(file_format)
    if file_format in {'docx', 'pptx', 'xlsx'}:
        try:
            meta_data = get_from_office_x(f'./tmp/{file_name}')
        except BaseException:
            print(f"Cannot read metadata from file {file_name}")
    if file_format in {'jpeg', 'jpg', 'raw', 'tiff'}:
        try:
            meta_data = get_exif_data(f'./tmp/{file_name}')
        except BaseException:
            print(f"Cannot read metadata from file {file_name}")

    return meta_data
