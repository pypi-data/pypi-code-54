from collections import Counter
import numpy as np


def to_categorical_list(input_list):
    result = [0] * len(input_list)
    keys = {}
    for idx, el in enumerate(input_list):
        if el in keys:
            result[idx] = keys[el]
        else:
            keys[el] = len(keys)
            result[idx] = keys[el]
    return result, keys


def to_categorical_list_2d(input_list, num_of_sort=-1):
    num_list, keys = to_categorical_list(input_list)
    if num_of_sort <= 0:
        result = np.zeros(shape=(len(input_list), len(keys)))
    else:
        result = np.zeros(shape=(len(input_list), num_of_sort))
    for i in range(len(input_list)):
        result[i][num_list[i]] = 1
    return result.astype(int), keys


def change_categorical_pandas(input_pandas):
    num_object = 0
    num_other = 0
    strange_dict = {}
    key_result = {}
    for col_name, col_contents in input_pandas.iteritems():
        tp = col_contents.dtype
        if tp != float and tp != int:
            try:
                tmp = col_contents.astype(float)
                input_pandas[col_name] = tmp
            except ValueError:
                if tp == object:
                    num_object += 1
                else:
                    num_other += 1
                strange_dict[col_name] = Counter(col_contents)
    print("number of object column\t", num_object)
    print("number of other column\t", num_other)
    while True:
        print("The number of columns which are not int or float :", len(strange_dict))
        print("Do you want to inspect?")
        print("y : yes / n : no / s : list of columns name")
        var = input()
        if var == "y":
            for key, value in strange_dict.items():
                while True:
                    print(key, "\t: number of sort : ", len(value))
                    var = input("categorize(1) / want to see(2) / Don't do anything(3) : ")
                    if var == "1":
                        result3, my_keys = to_categorical_list(input_pandas[key])
                        input_pandas[key] = result3
                        key_result[key] = my_keys
                        break
                    elif var == "2":
                        print(value)
                    elif var == "3":
                        break
                    else:
                        print("Press one of three options (1,2,3)")
            break
        elif var == "n":
            break
        elif var == "s":
            print(strange_dict.keys())
        else:
            print("Press one of three options (y, n, s)")
    return key_result
