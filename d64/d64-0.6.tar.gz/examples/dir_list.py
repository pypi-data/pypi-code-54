import sys

from d64 import DiskImage

with DiskImage(sys.argv[1]) as image:
    for line in image.directory():
        print(line)
