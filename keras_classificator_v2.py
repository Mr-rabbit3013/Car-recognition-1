import math
import os

from keras import applications
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

TRAIN_DIR = 'C:\\car_photos_299x299\\train'
VALID_DIR = 'C:\\car_photos_299x299\\validation'
IMG_SIZE = (299, 299)
BATCH_SIZE = 4
EPOCHS = 100

if __name__ == "__main__":
    num_train_samples = sum([len(files) for r, d, files in os.walk(TRAIN_DIR)])
    num_valid_samples = sum([len(files) for r, d, files in os.walk(VALID_DIR)])

    num_train_steps = math.floor(num_train_samples / BATCH_SIZE)
    num_valid_steps = math.floor(num_valid_samples / BATCH_SIZE)

    train_gen = ImageDataGenerator()
    val_gen = ImageDataGenerator(horizontal_flip=True, vertical_flip=True)

    train_batches = train_gen.flow_from_directory(TRAIN_DIR,
                                                  target_size=IMG_SIZE,
                                                  class_mode='categorical',
                                                  shuffle=True,
                                                  batch_size=BATCH_SIZE)
    val_batches = val_gen.flow_from_directory(VALID_DIR,
                                              target_size=IMG_SIZE,
                                              class_mode='categorical',
                                              shuffle=True,
                                              batch_size=BATCH_SIZE)

    model = applications.Xception(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))

    classes = list(iter(train_batches.class_indices))
    model.layers.pop()
    for layer in model.layers:
        layer.trainable = False
    last = model.layers[-1].output
    x = Dense(len(classes), activation="softmax")(last)

    finetuned_model = Model(model.input, x)
    finetuned_model.compile(optimizer=Adam(lr=0.0001),
                            loss='categorical_crossentropy',
                            metrics=['accuracy'])

    for c in train_batches.class_indices:
        classes[train_batches.class_indices[c]] = c
    finetuned_model.classes = classes

    finetuned_model.summary()
    model.summary()

    early_stopping = EarlyStopping(patience=10)
    checkpointer = ModelCheckpoint('Xception_best.h5', verbose=1, save_best_only=True)

    finetuned_model.fit_generator(train_batches,
                                  steps_per_epoch=num_train_steps,
                                  epochs=EPOCHS,
                                  callbacks=[early_stopping, checkpointer],
                                  validation_data=val_batches,
                                  validation_steps=num_valid_steps)
    finetuned_model.save('Xception_final.h5')
