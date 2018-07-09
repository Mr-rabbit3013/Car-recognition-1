import glob
import os

from PIL import Image
from resizeimage import resizeimage

ORIGINAL_FOLDER = 'C:\\car_photos_224x224\\train'
RESIZED_FOLDER = 'C:\\car_photos_224x224\\train'

HEIGHT = 224
WIDTH = 224


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
    if image_width < WIDTH or image_height < HEIGHT:
        print('Removing file because is too small: ' + str(source))
        image.close()
        f.close()
        os.remove(source)
        return
    try:
        print('Resize file: ' + str(source))
        cover = resizeimage.resize_cover(image, [HEIGHT, WIDTH])
        cover.save(target, image.format)
    except Exception as exception:
        print('Unexpected exception: ' + str(exception))
    image.close()
    f.close()


def resize_directory_recursively(source):
    for directory in glob.iglob(source + '/*/'):
        resize(directory, directory)


if __name__ == '__main__':
    resize_directory_recursively(ORIGINAL_FOLDER)
