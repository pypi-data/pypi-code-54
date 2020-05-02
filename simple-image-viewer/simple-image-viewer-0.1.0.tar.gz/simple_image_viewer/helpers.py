
#!/usr/bin/env python

##############################################################################
#
# Copyright (c) 2020 Saeid Hosseinipoor <https://saeid-h.github.io/>
# All rights reserved.
# Licensed under the MIT License
#
##############################################################################

from __future__ import absolute_import, division, print_function

import os, glob

os.environ['TK_SILENCE_DEPRECATION'] = '1'

def getListOfFiles(dirName, masks=['*.png'], sudirectories=False):
	listOfFile = os.listdir(dirName)
	allFiles = list()
	for mask in masks:
		allFiles += glob.glob(dirName+mask)
	for entry in listOfFile:
		fullPath = os.path.join(dirName, entry) + '/'
		if os.path.isdir(fullPath) and sudirectories:
			allFiles += getListOfFiles(fullPath, masks, sudirectories)
	
	return allFiles
	

if __name__ == "__main__":
	pass