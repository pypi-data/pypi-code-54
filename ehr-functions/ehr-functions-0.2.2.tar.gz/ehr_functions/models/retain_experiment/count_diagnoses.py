from collections import Counter
from ehr_functions.paths import DATA
import pandas as pd
import numpy as np
import os


def __get_data():
    folder = os.path.join(DATA, 'interim', 'retain')

    data_train_df = pd.read_pickle(os.path.join(folder, 'data_train.pkl'))
    data_test_df = pd.read_pickle(os.path.join(folder, 'data_test.pkl'))
    y_train = pd.read_pickle(os.path.join(folder, 'target_train.pkl'))['target'].values
    y_test = pd.read_pickle(os.path.join(folder, 'target_test.pkl'))['target'].values
    x_train = data_train_df['codes'].values
    x_test = data_test_df['codes'].values

    return x_train, y_train, x_test, y_test


def __get_num_codes(x_train, x_test):
    codes_train = set([code for patient in x_train for encounter in patient for code in encounter])
    codes_test = set([code for patient in x_test for encounter in patient for code in encounter])

    all_codes = codes_train | codes_test
    return len(all_codes)


def __transform_into_counts(patients, num=None):
    patients = patients.tolist()
    for p, patient in enumerate(patients):
        counts = Counter([code for encounter in patient for code in encounter])
        patients[p] = [0 if i not in counts else counts[i] for i in range(num)]

    return np.asarray(patients)


def get_count_data():
    x_train, y_train, x_test, y_test = __get_data()

    num_codes = __get_num_codes(x_train, x_test)
    print('Num Codes', num_codes)

    x_train = __transform_into_counts(x_train, num=num_codes)
    x_test = __transform_into_counts(x_test, num=num_codes)

    return x_train, y_train, x_test, y_test


if __name__ == '__main__':
    get_count_data()
