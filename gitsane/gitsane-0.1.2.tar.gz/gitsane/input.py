"""
Read, parse, and sort json file object

Return:
    schema, TYPE: json

"""
import os
import json
import inspect
from gitsane import logger


class ParseInputFile():
    """Read, parse, and sort json file object"""
    def __init__(self, filename):
        self.jsonobject = self.read(filename)

    def read(self, fname):
        """Read json file object from local fs"""
        if os.path.exists(fname):
            try:
                with open(fname, 'r') as f1:
                    f2 = json.loads(f1.read())
                return f2
            except OSError:
                fx = inspect.stack()[0][2]
                logger.exception(f'{fx}: Failure to read {fname} from local filesystem')
        return None

    def parse(self, fname=None):
        """Returns sorted, complex json object"""
        jobject = self.jsonobject if fname is None else self.read(fname)
        try:
            s = sorted(jobject, key=lambda x: x['location'], reverse=False)
        except KeyError:
            return jobject    # return unsorted object
        return s
