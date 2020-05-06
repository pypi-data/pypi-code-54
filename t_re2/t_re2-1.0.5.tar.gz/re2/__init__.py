# coding: utf-8

import os
import shutil


# copy so file to /usr/local/lib
dependent_files = '/usr/local/lib/libre2.so.7'
if not os.path.isfile(dependent_files):
    if not os.path.exists(os.path.dirname(dependent_files)):
        os.makedirs(os.path.dirname(dependent_files))
    shutil.copy2('./libre2.so.7', dependent_files)
