import re
from pathlib import Path
import zwutils.fileutils as fileutils
class Pdf(object):
    def __init__(self, pth):
        self._path = Path(pth)
    
    def meta_from_filename(self, r, arr):
        m = re.match( r, self.path.name, re.M|re.I)
        rtn = None
        if m and len(m.groups()) == len(arr):
            rtn = {}
            for i in range( len(m.groups()) ):
                rtn[arr[i]] = m.group(i+1)
            rtn['md5'] = fileutils.md5(str(self.path))
        return rtn
    
    @property
    def path(self):
        return self._path
