# import files.readUtilss
# import os

# print(os.getcwd())
# files.readUtilss.read_file('test.txt')


def read_file(path):
    print(path)
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        print("file doesn't exist")
