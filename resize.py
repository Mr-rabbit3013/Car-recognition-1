import glob
import os

from PIL import Image

ORIGINAL_FOLDER = 'C:\\Private\\BMW\\car_photos\\'

HEIGHT = 224
WIDTH = 224

TOLERANCE_RATIO = 0.10  # range [0 - 1]


def square(source, target):
    f = open(source, 'r+b')
    image = Image.open(f)
    image_width, image_height = image.size
    try:
        if image_height == image_width:
            return
        print('Squaring image: ' + str(source))
        image = Image.open(source)
        if image_width < image_height:
            up_difference = int((image_height - image_width) / 2)
            down_difference = round((image_height - image_width) / 2)
            box = (0, up_difference, image_width, down_difference + image_width)
            cropped = image.crop(box)
            cropped.save(target)
        if image_width > image_height:
            left_difference = int((image_width - image_height) / 2)
            right_difference = int((image_width - image_height) / 2)
            box = (left_difference, 0, right_difference + image_height, image_height)
            cropped = image.crop(box)
            cropped.save(target)
    except Exception as exception:
        print('Unexpected exception: ' + str(exception))
    image.close()
    f.close()


def resize(source, target):
    if not os.path.exists(target):
        os.makedirs(target)

    files_number = len(os.listdir(source))
    index = 1
    for picture_file in os.listdir(source):
        print('File ' + str(index) + '/' + str(files_number) + '  ' + picture_file)
        file = source + picture_file
        single_resize(file, file)
        index += 1


def single_resize(source, target):
    f = open(source, 'r+b')
    image = Image.open(f)
    image_width, image_height = image.size
    if image_width * TOLERANCE_RATIO + image_width < WIDTH or image_height * TOLERANCE_RATIO + image_height < HEIGHT:
        print('Removing file because is too small: ' + str(source))
        image.close()
        f.close()
        os.remove(source)
        return
    try:
        print('Resize file: ' + str(source))
        resized = image.resize((HEIGHT, WIDTH))
        resized.save(target, image.format)
    except Exception as exception:
        print('Unexpected exception: ' + str(exception))
    image.close()
    f.close()


def resize_directory_recursively(source):
    for directory in glob.iglob(source + '/*/'):
        resize(directory, directory)


if __name__ == '__main__':
    resize_directory_recursively(ORIGINAL_FOLDER)
