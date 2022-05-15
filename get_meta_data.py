import requests
import zipfile
import xml.etree.ElementTree as ET
import exif

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
    data = exif.parse(file_name)
    return data

def get(url):
    file_name = url.split('/')[-1]
    file = open(f'./tmp/{file_name}', "wb")
    ufr = requests.get(url)
    file.write(ufr.content)
    file.close

    meta_data = dict()
    file_format = file_name.split('.')[-1]
    if file_format == 'docx' or file_format == 'pptx' or file_format == 'xlsx':
        meta_data = get_from_office_x(f'./tmp/{file_name}')
    if file_format == 'jpeg' or file_format == 'tiff' or file_format == 'raw':
        meta_data = get_exif_data(f'./tmp/{file_name}')

    return meta_data
