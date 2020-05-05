#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 01:47:17 2020

@author: jkl
"""

import os
import requests

def checkExe(dirname):
    exes = ['R2.exe','cR2.exe','R3t.exe','cR3t.exe','gmsh.exe']
    for exe in exes:
        fname = os.path.join(dirname, exe)
        if os.path.exists(fname) is not True:
            print('Downloading ' + exe + '...', end='', flush=True)
            response = requests.get("https://gitlab.com/hkex/pyr2/-/raw/master/src/resipy/exe/" + exe)
            with open(fname, 'wb') as f:
                f.write(response.content)
            print('done')
                
checkExe(os.path.join(apiPath, 'exe'))

