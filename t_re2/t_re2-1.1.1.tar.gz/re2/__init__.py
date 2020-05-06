# coding: utf-8

import os
import shutil

so_file_path = 't_re2.conf'
so_dir_path = '/etc/ld.so.conf.d'

# 0. 在/etc/ld.so.conf.d中, 判断是否存在t_re2.conf文件
if so_file_path not in set(os.listdir(so_dir_path)):
    # 1. 新增一个配置文件
    # todo 这里应该还会有一个问题, 如果在虚拟环境1中新增了 t_re2.conf配置,
    #  那么再虚拟环境2中则不会再将t_re2.conf的配置内容指向虚拟环境2中的so目录, 还是会继续使用虚拟环境1的so目录
    with open(os.path.join(so_dir_path, so_file_path), 'w') as fp:
        # 2. 将该目录的绝对路径加入到查找so文件的配置中
        fp.write(os.path.dirname(__file__))
    # 3. sudo /sbin/ldconfig
    os.popen('/sbin/ldconfig')
