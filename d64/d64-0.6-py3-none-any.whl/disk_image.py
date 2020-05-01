import os
import os.path
import shutil
import tempfile

from .d64_image import D64Image


class DiskImage(object):
    raw_modes = {'r': 'rb', 'w': 'r+b'}

    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = self.raw_modes.get(mode, 'rb')

    def __enter__(self):
        if self.mode == 'r+b':
            self.org_filename = self.filename
            tempf = tempfile.NamedTemporaryFile(prefix='d64-', dir=os.path.dirname(self.filename),
                                                delete=False)
            # copy existing file to temporary
            with open(self.org_filename, 'rb') as inh:
                shutil.copyfileobj(inh, tempf)
            tempf.close()
            self.filename = tempf.name

        self.image = D64Image(self.filename)
        self.image.open(self.mode)
        return self.image

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.image.close()

        if self.mode == 'r+b':
            if exc_type is None:
                # update original with modified file
                os.replace(self.filename, self.org_filename)
            else:
                os.remove(self.filename)
