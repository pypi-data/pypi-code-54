import os
import sys
from pathlib import Path
from qaboard.utils import redirect_std_streams

print('BEFORE')
with redirect_std_streams(Path('log.txt')):
    print("ON STDOUT")
    print("ON STDOUT", file=sys.stderr)
    os.system('echo this is also redirected')
    # check we see the 3 prints on the terminal
    # check we see the 3 prints in a file
    # colors...
    # check: local, LSF, windows
print('AFTER')
