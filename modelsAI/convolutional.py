import time
import keras.models
import numpy as np
import os
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.callbacks as callbacks
import tensorflow.keras.losses as losses
import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

class ConvolutionalModelTeaching:
    def __init__(self, dir_path):
        start_time = time.time()
        self.noFiles = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
        self.entries = os.listdir(dir_path)
        self.dir_path = dir_path
        self.x_data, self.y_data = self.get_data()

        filePath = f'C:\\aidata\\data_size_13_norm_out\\20230505-174522.npz'
        with open(filePath, 'rb') as f:
            self.y_data = np.load(f)

        end_time = time.time()
        print(f'It took {end_time - start_time} second(s) to load data.')

        model = self.build_model(16, 4)
        loss = losses.SparseCategoricalCrossentropy()
        model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
        model.summary()
        checkpoint_filepath = '/tmp/checkpoint/'
        model_checkpointing_callback = ModelCheckpoint(
            filepath=checkpoint_filepath,
            save_best_only=True,
        )
        model.fit(self.x_data, self.y_data,
                  batch_size=2048,
                  epochs=10,
                  verbose=1,
                  validation_split=0.1,
                  callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                             callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4),
                             model_checkpointing_callback])

        model.save('model.h5')

    def normalize_output(self, y_data):
        positiveBase = np.amax(y_data)
        negativeBase = np.amin(y_data)
        negativeBase = 0 - negativeBase

        base = positiveBase + negativeBase
        new_y_data = y_data + negativeBase
        new_y_data = new_y_data / base

        filePath = f'data_size_13_norm_out\\{time.strftime("%Y%m%d-%H%M%S")}.npz'
        with open(filePath, 'wb') as f:
            np.save(f, new_y_data)

        return np.array(new_y_data)



    def get_data(self):
        x_train = []
        y_train = []
        for i in range(self.noFiles):
            with open(f'{dir_path}\\{self.entries[i]}', 'rb') as f:
                packageInput = np.load(f)
                packageOutput = np.load(f)
                x_train.append(packageInput)
                y_train.append(packageOutput)
        return np.concatenate(x_train, axis=0), np.concatenate(y_train, axis=0)

    def build_model(self, conv_size, conv_depth):
        board3d = layers.Input(shape=(13, 8, 8))
        x = board3d
        for _ in range(conv_depth):
            x = layers.Conv2D(filters=conv_size, kernel_size=3,
                              padding='same', activation='relu')(x)
        x = layers.Flatten()(x)
        x = layers.Dense(64, 'relu')(x)
        x = layers.Dense(1, 'sigmoid')(x)
        return models.Model(inputs=board3d, outputs=x)

    def build_model_residual(self, conv_size, conv_depth):
        board3d = layers.Input(shape=(13, 8, 8))

        # adding the convolutional layers
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(board3d)
        for _ in range(conv_depth):
            previous = x
            x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Activation('relu')(x)
            x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(x)
            x = layers.BatchNormalization()(x)
            x = layers.Add()([x, previous])
            x = layers.Activation('relu')(x)
        x = layers.Flatten()(x)
        x = layers.Dense(1, 'sigmoid')(x)

        return models.Model(inputs=board3d, outputs=x)


if __name__ == '__main__':
    dir_path = r'C:\\aidata\\data_size_13'
    ConvolutionalModelTeaching(dir_path)
