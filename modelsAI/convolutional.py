import numpy as np
import os

class ConvolutionalModel:
    def __init__(self, dir_path):
        self.noFiles = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])
        self.entries = os.listdir(dir_path)
        self.dir_path = dir_path
        self.x_data, self.y_data = self.get_data()
        print(f'Packages input shape: {np.shape(self.x_data)}')
        print(f'Packages output shape: {np.shape(self.y_data)}')
        print(self.x_data[0])
        print(self.y_data[0])

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


if __name__ == '__main__':
    dir_path = r'data'
    ConvolutionalModel(dir_path)
