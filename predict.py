import os

import numpy as np
from keras.models import load_model
from keras.preprocessing import image

MODEL_NAME = 'conv_network_final.h5'
MODEL_PATH = 'D:\\BMW\\skrypts\\' + MODEL_NAME
IMG_WIDTH, IMG_HEIGHT = 224, 224
SOURCE_IMAGE_DIRECTORY = 'D:\\BMW\\e60\\original'
CAR_DIRECTORY = 'D:\\BMW\\e60\\car'
NO_CAR_DIRECTORY = 'D:\\BMW\\e60\\no_car'
CLASSIFY_RATIO = 0.95


def predict_single(model, image_path):
    img = image.load_img(image_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    return model.predict(images, batch_size=10)


def predict_directory(source_directory):
    model = load_model(MODEL_NAME)
    index = 0
    files_number = len(os.listdir(source_directory))
    for picture_file in os.listdir(source_directory):
        index += 1
        print(f'Processing file {str(index)}/{files_number}')
        try:
            classes = predict_single(model, source_directory + '/' + picture_file)
            if classes[0][0] > CLASSIFY_RATIO:
                os.rename(source_directory + '/' + picture_file, NO_CAR_DIRECTORY + '/' + picture_file)
            if classes[0][1] > CLASSIFY_RATIO:
                os.rename(source_directory + '/' + picture_file, CAR_DIRECTORY + '/' + picture_file)
        except:
            print('Some exception')


if __name__ == '__main__':
    model = load_model(MODEL_NAME)
    predict_directory(SOURCE_IMAGE_DIRECTORY)
    #predict_single(model, 'C:\\Users\\wieczoma\\Desktop\\BMW\\car_photos_224x224\\train\\outside\\00001.jpg')