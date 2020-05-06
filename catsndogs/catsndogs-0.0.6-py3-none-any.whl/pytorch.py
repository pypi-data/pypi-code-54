import torch
import os
import glob
from torch.utils.data import Dataset
from catsndogs.data import get_training_data, get_test_data
from skimage import io

class CatsNDogsData():
    def __init__(self, mode="training"):
        if mode == "training":
            self.data_dir = get_training_data()
        else:
            self.data_dir = get_test_data()

        self._load_data()

    def _load_data(self):
        self.files = glob.glob(os.path.join(self.data_dir, "*.jpg"))
        self.classes = [int(os.path.basename(f)[0].isupper()) for f in self.files]

        self.x = torch.zeros(len(self.files), 3, 64, 64)
        self.y = torch.zeros(len(self.files), 1)
        for i, (f, c) in enumerate(zip(self.files, self.classes)):
            self.x.data[i, :, :] = torch.tensor(io.imread(f)).float().transpose(0, -1) / 256.0
            self.y.data[i, 0] = c
        self.x.data = -1.0 + 2.0 * self.x.data

    def __len__(self):
        return self.x.size()[0]

    def __getitem__(self, index):
        return (self.x[index], self.y[index])

training_data = CatsNDogsData("training")
test_data = CatsNDogsData("test")
