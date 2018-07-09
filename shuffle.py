import os
import glob
from random import shuffle

FOLDER = 'C:\\car_photos_224x224\\train'


def shuffle_directory_recursively(source):
    for directory in glob.iglob(source + '/*/'):
        shuffle_single_directory(directory)


def shuffle_single_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    files_number = len(os.listdir(directory))
    index = 1
    pictures = os.listdir(directory)
    shuffle(pictures)
    for picture_file in pictures:
        print('File ' + str(index) + '/' + str(files_number) + '  ' + picture_file + '. New name: ' + str(index).zfill(5) + '.jpg')
        old_name = directory + '/' + picture_file
        new_name = directory + '/' + str(index).zfill(5) + '.jpg'
        os.rename(old_name, new_name)
        index += 1


if __name__ == '__main__':
    shuffle_directory_recursively(FOLDER)