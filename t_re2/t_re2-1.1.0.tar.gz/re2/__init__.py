# coding: utf-8

import os
import shutil

so_file_path = 't_re2.conf'
so_dir_path = '/etc/ld.so.conf.d'

# 0. 在/etc/ld.so.conf.d中, 判断是否存在t_re2.conf文件
if so_file_path not in set(os.listdir(so_dir_path)):
    # 1. 新增一个配置文件
    with open(os.path.join(so_dir_path, so_file_path), 'w') as fp:
        # 2. 将该目录的绝对路径加入到查找so文件的配置中
        fp.write(os.path.dirname(__file__))
    # 3. sudo /sbin/ldconfig
    os.popen('/sbin/ldconfig')
