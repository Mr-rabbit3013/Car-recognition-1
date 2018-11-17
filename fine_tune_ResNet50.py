from __future__ import print_function

import matplotlib.pyplot as plt
from keras import Sequential
from keras.applications import ResNet50
from keras.callbacks import EarlyStopping, ModelCheckpoint, CSVLogger
from keras.layers import Dense, AveragePooling2D, Flatten
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

IMAGE_SIZE = 224
TARGET_IMAGE_SIZE = (IMAGE_SIZE, IMAGE_SIZE)
TRAIN_DATA_DIR = 'D:\\BMW photos\\car_photos'
#TEST_DATA_DIR = 'C:\\Private\\BMW\\car_photos_224x224\\test'
BATCH_SIZE = 8
EPOCHS = 100


def prepare_data():
    train_datagen = ImageDataGenerator(
        validation_split=0.2,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DATA_DIR,
        target_size=TARGET_IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training',
        shuffle=True)
    validation_generator = train_datagen.flow_from_directory(
        TRAIN_DATA_DIR,
        target_size=TARGET_IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=True)

    # test_datagen = ImageDataGenerator(rescale=1./255)
    # test_generator = test_datagen.flow_from_directory(
    #     TEST_DATA_DIR,
    #     target_size=(IMG_WIDTH, IMG_HEIGHT),
    #     batch_size=BATCH_SIZE,
    #     class_mode='categorical',
    #     shuffle=True)
    # return train_generator, validation_generator, test_generator
    return train_generator, validation_generator


def show_history(history):
    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()


def training():
    train_generator, validation_generator = prepare_data()
    # train_generator, validation_generator, test_generator = prepare_data()

    resnet50_network = ResNet50(include_top=False,
                            weights='imagenet',
                            input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3))

    for layer in resnet50_network.layers[:-3]:
        layer.trainable = False

    model = Sequential()
    model.add(resnet50_network)
    model.add(AveragePooling2D((7, 7), name='avg_pool'))
    model.add(Flatten())
    model.add(Dense(train_generator.class_indices.items().__len__(), activation='softmax'))
    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.001),
                  metrics=['accuracy'])

    early_stopping = EarlyStopping(patience=10)
    checkpointer = ModelCheckpoint(filepath='car_resNet50_best.h5', verbose=0, save_best_only=True)

    csv_logger = CSVLogger('ResNet50_training_log.csv', append=True, separator=';')

    history = model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.samples / train_generator.batch_size,
        epochs=EPOCHS,
        callbacks=[early_stopping, checkpointer, csv_logger],
        validation_data=validation_generator,
        validation_steps=validation_generator.samples / validation_generator.batch_size)

    # evaluate_scores = model.evaluate_generator(generator=test_generator)

    model.save('car_resNet50_final.h5')
    model.sample_weights('resNet50_weights')
    show_history(history)


if __name__ == '__main__':
    training()
