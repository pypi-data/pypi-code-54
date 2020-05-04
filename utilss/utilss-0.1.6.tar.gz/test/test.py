from utilss import getMax
from utilss import getMin

test = getMax.__file__
print(getMax.__author__)

import re
print(re.__file__)

try:
    import gege
except ImportError:
    print("module not found")

print("end")