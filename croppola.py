import os, requests
from PIL import Image

ORIGINAL_FOLDER = 'D:\\original'
CROPPED_FOLDER = 'D:\\original'

# This is the URL
URL = 'http://croppola.com/croppola/image.jpg?aspectRatio=1:1%maximumWidth=100%&maximumHeight=100%&algorithm=croppola'


def crop(source, target):
    if not os.path.exists(target):
        os.makedirs(target)

    files_number = len(os.listdir(source))
    index = 0
    for picture_file in os.listdir(source):
        index += 1
        image = Image.open(ORIGINAL_FOLDER + '/' + picture_file)
        width, height = image.size
        if width == height:
            continue
        print('File ' + str(index) + '/' + str(files_number) + '  ' + picture_file)
        data = open(source + '/' + picture_file, 'rb')
        res = requests.post(URL, data=data, headers={'User-Agent': 'py'})
        data.close()
        if res.status_code == 200:
            f = open(target + '/' + picture_file, 'wb')
            f.write(res.content)
        else:
            print('Error ' + str(res.status_code) + ' ' + str(res.reason))


def single_crop(source, target):
    print('Cropping file: ' + str(source))
    data = open(source, 'rb')
    res = requests.post(URL, data=data, headers={'User-Agent': 'py'})
    data.close()
    if res.status_code == 200:
        f = open(target, 'wb')
        f.write(res.content)
    else:
        print('Error ' + str(res.status_code) + ' ' + str(res.reason))


if __name__ == '__main__':
    crop(ORIGINAL_FOLDER, CROPPED_FOLDER)
