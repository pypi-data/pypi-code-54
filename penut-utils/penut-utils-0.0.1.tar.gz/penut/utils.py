import os
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

def to_categorical(arr):
    s = set(arr)
    d = dict(zip(list(s), range(len(s))))
    rtn = list(map(d.get, arr))

    return np.array(rtn), d

def plot_labels(data, labels, xlim=None, ylim=None, save=None):
    [plt.plot(data[lab], label=lab) for lab in labels]
    plt.legend()
    
    if xlim:
        plt.xlim(*xlim)
    
    if ylim:
        plt.ylim(*ylim)
    
    if save:
        plt.savefig(save)
        plt.clf()
    
    return plt

def walk_dir(target_dir, return_file_name=False, return_dir_name=False):
    for dir_path, _, file_list in os.walk(target_dir):
        for file_name in file_list:
            full_path = os.path.join(dir_path, file_name)
            rtn = [full_path]
            if return_file_name:
                rtn.append(file_name)
            if return_dir_name:
                rtn.append(dir_path)
            yield rtn

class TimeCost:
    def __init__(self, msg='Time Cost', verbose=True):
        self.ts = None
        self.verbose = verbose
        self.msg = msg
    
    def __enter__(self):
        self.ts = dt.datetime.now()
    
    def __exit__(self, *args):
        self.ts = dt.datetime.now() - self.ts
        if self.verbose:
            print(f'{self.msg}: {self.ts.total_seconds()}s')

if __name__ == "__main__":
    # print(to_categorical([1, 2, 3, 2, 1]))
    # print(to_categorical(['香草', '巧克力', '草莓', '巧克力', '香草']))
    # with TimeCost('Sleep Time'):
    #     import time
    #     time.sleep(1)
    for [fp] in walk_dir('./'):
        print(fp)
