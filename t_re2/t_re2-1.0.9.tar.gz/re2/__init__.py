# coding: utf-8

import os
import shutil

# copy so file to /usr/local/lib
# os.path.join(os.path.dirname(__file__), 'libre2.so.7')
# add path

so_file_path = 't_re2.conf'
so_dir_path = '/etc/ld.so.conf.d'

# 0. 在/etc/ld.so.conf.d中, 判断是否存在t_re2.conf文件
if so_file_path not in set(os.listdir(so_dir_path)):
    # 1. 新增一个文件
    with open(os.path.join(so_dir_path, so_file_path), 'w') as fp:
        # 2. 文件内容为 os.path.join(os.path.dirname(__file__), 'libre2.so.7')
        fp.write(os.path.dirname(__file__))
    # 3. sudo /sbin/ldconfig
    os.popen('/sbin/ldconfig')

# dependent_files = '/usr/local/lib/libre2.so.7'
# if not os.path.isfile(dependent_files):
#     if not os.path.exists(os.path.dirname(dependent_files)):
#         os.makedirs(os.path.dirname(dependent_files))
#     shutil.copy2(os.path.join(os.path.dirname(__file__), 'libre2.so.7'), dependent_files)
