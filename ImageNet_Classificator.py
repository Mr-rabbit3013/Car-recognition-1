import matplotlib.pyplot as plt
import numpy as np
from keras.applications import vgg16, vgg19, inception_v3, inception_resnet_v2, resnet50, mobilenet, densenet, xception
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img

WIDTH = 224
HEIGHT = 224

car_labels = ['minivan', 'limousine', 'grille', 'car_wheel', 'beach_wagon']


class Classificator:

    def __init__(self):
        self

    def xception_classificator(self, image_path):
        xception_model = xception.Xception(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = xception.preprocess_input(image_batch.copy())
        predictions = xception_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def mobilenet_classificator(self, image_path):
        mobilenet_model = mobilenet.MobileNet(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = mobilenet.preprocess_input(image_batch.copy())
        predictions = mobilenet_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def vgg16_classificator(self, image_path):
        vgg16_model = vgg16.VGG16(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = vgg16.preprocess_input(image_batch.copy())
        predictions = vgg16_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def vgg19_classificator(self, image_path):
        vgg19_model = vgg19.VGG19(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = vgg19.preprocess_input(image_batch.copy())
        predictions = vgg19_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def inception_v3_classificator(self, image_path):
        inception_model = inception_v3.InceptionV3(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = inception_v3.preprocess_input(image_batch.copy())
        predictions = inception_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def inception_resnet_v2_classificator(self, image_path):
        inception_resnet_v2_model = inception_resnet_v2.InceptionResNetV2(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = inception_resnet_v2.preprocess_input(image_batch.copy())
        predictions = inception_resnet_v2_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def resnet50_classificator(self, image_path):
        resnet_model = resnet50.ResNet50(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = resnet50.preprocess_input(image_batch.copy())
        predictions = resnet_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)

    def denseNet201_classificator(self, image_path):
        denseNet201_model = densenet.DenseNet201(weights='imagenet')
        filename = image_path
        original = load_img(filename, target_size=(WIDTH, HEIGHT))
        plt.imshow(original)
        numpy_image = img_to_array(original)
        plt.imshow(np.uint8(numpy_image))
        image_batch = np.expand_dims(numpy_image, axis=0)
        plt.imshow(np.uint8(image_batch[0]))
        processed_image = densenet.preprocess_input(image_batch.copy())
        predictions = denseNet201_model.predict(processed_image)
        label = decode_predictions(predictions)
        return sorted(label[0], key=lambda x: x[2], reverse=True)
