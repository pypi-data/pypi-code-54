# -*- coding: utf-8 -*-
"""
@author:XuMing（xuming624@qq.com)
@description: 
"""

from pathlib import Path

from mingdongtextsim.similarity import Similarity, SearchSimilarity, SimType
from mingdongtextsim.utils.logger import set_log_level
from mingdongtextsim.vector import EmbType, Vector

USER_DIR = Path.expanduser(Path('~')).joinpath('.mingdongtextsim')
if not USER_DIR.exists():
    USER_DIR.mkdir()
USER_DATA_DIR = USER_DIR.joinpath('datasets')
if not USER_DATA_DIR.exists():
    USER_DATA_DIR.mkdir()

VEC = Vector()
encode = VEC.encode
