from __future__ import print_function

from keras.applications import ResNet50
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

IMG_WIDTH, IMG_HEIGHT = 224, 224
TRAIN_DATA_DIR = 'C:\\Private\\BMW\\car_photos_224x224\\train'
VALIDATION_DATA_DIR = 'C:\\Private\\BMW\\car_photos_224x224\\validation'
BATCH_SIZE = 8
EPOCHS = 1000


def training():
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    train_generator = train_datagen.flow_from_directory(
        TRAIN_DATA_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True)

    validation_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')
    validation_generator = validation_datagen.flow_from_directory(
        VALIDATION_DATA_DIR,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=True)

    model = ResNet50(include_top=True,
                     weights=None,
                     input_shape=(IMG_WIDTH, IMG_HEIGHT, 3),
                     classes=train_generator.class_indices.items().__len__())
    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=0.001),
                  metrics=['accuracy'])

    early_stopping = EarlyStopping(patience=10)
    checkpointer = ModelCheckpoint(filepath='filter_network_best.h5', verbose=2, save_best_only=True)

    model.fit_generator(
        train_generator,
        steps_per_epoch=train_generator.samples / train_generator.batch_size,
        epochs=EPOCHS,
        callbacks=[early_stopping, checkpointer],
        validation_data=validation_generator,
        validation_steps=validation_generator.samples / validation_generator.batch_size)

    # Save the model
    model.save('filter_network_final.h5')


if __name__ == '__main__':
    training()
