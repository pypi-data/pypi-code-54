from os import makedirs
from os.path import exists
from datetime import datetime


def touch_dir(dir_path):
    if not (exists(dir_path)):
        makedirs(dir_path)


def datetime_4_directory_string():
    now = datetime.now()
    return "{}-{}-{}_{}-{}-{}".format(
        now.year,
        str(now.month).zfill(2),
        str(now.day).zfill(2),
        str(now.hour).zfill(2),
        str(now.minute).zfill(2),
        str(now.second).zfill(2))


def time_string():
    now = datetime.now()
    return "{}:{}:{}".format(
        str(now.hour).zfill(2),
        str(now.minute).zfill(2),
        str(now.second).zfill(2))


def date_string():
    now = datetime.now()
    return "{}/{}/{}".format(
        now.year,
        str(now.month).zfill(2),
        str(now.day).zfill(2))


def datetime_string():
    return date_string() + " at " + time_string()



