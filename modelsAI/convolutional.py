import numpy as np
import os
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.utils as utils
import tensorflow.keras.optimizers as optimizers
import tensorflow.keras.callbacks as callbacks


class ConvolutionalModelTeaching:
    def __init__(self, dir_path):
        self.noFiles = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
        self.entries = os.listdir(dir_path)
        self.dir_path = dir_path
        self.x_data, self.y_data = self.get_data()
        # self.x_data = np.concatenate((self.x_data, self.x_data), axis=0)
        # self.y_data = np.concatenate((self.y_data, self.y_data), axis=0)
        # self.x_data = np.concatenate((self.x_data, self.x_data), axis=0)
        # self.y_data = np.concatenate((self.y_data, self.y_data), axis=0)
        # self.x_data = np.concatenate((self.x_data, self.x_data), axis=0)
        # self.y_data = np.concatenate((self.y_data, self.y_data), axis=0)
        # self.x_data = np.concatenate((self.x_data, self.x_data), axis=0)
        # self.y_data = np.concatenate((self.y_data, self.y_data), axis=0)
        # self.x_data = np.concatenate((self.x_data, self.x_data), axis=0)
        # self.y_data = np.concatenate((self.y_data, self.y_data), axis=0)
        print(f'Packages input shape: {np.shape(self.x_data)}')
        print(f'Packages output shape: {np.shape(self.y_data)}')
        # model = self.build_model(32, 4)
        # model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
        # model.summary()
        # model.fit(self.x_data, self.y_data, batch_size=2048, epochs=1000, verbose=1, validation_split=0.1,
        #           callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
        #                      callbacks.EarlyStopping(monitor='loss', patience=1000, min_delta=0.0001)])
        #
        # model.save('model.h5')

    def get_data(self):
        x_train = []
        y_train = []
        for i in range(self.noFiles):
            with open(f'{dir_path}\\{self.entries[i]}', 'rb') as f:
                packageInput = np.load(f)
                packageOutput = np.load(f)
                print(f'Package {self.entries[i]} input shape: {np.shape(packageInput)}')
                print(f'Package {self.entries[i]} output shape: {np.shape(packageOutput)}')
                x_train.append(packageInput)
                y_train.append(packageOutput)
        return np.concatenate(x_train, axis=0), np.concatenate(y_train, axis=0)

    def build_model(self, conv_size, conv_depth):
        board3d = layers.Input(shape=(4, 8, 8))

        # convolutional layers
        for _ in range(conv_depth):
            x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='sigmoid')(board3d)
            x = layers.Flatten()(x)
            x = layers.Dense(64, 'relu')(x)
            x = layers.Dense(1, 'sigmoid')(x)

        return models.Model(inputs=board3d, outputs=x)


if __name__ == '__main__':
    dir_path = r'data'
    ConvolutionalModelTeaching(dir_path)
