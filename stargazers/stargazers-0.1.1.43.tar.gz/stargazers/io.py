import cv2
import numpy as np
import re

LSB_UNSIGNED_INTEGER = "LSB_UNSIGNED_INTEGER"
PC_REAL = "PC_REAL"
# will need to fix this eventually, since these are acting as global
# variables for the eval() inside ImgParser


class ImgParser:
    # all these should be moved to a metaclass to handle jsut defining the
    # attributes here and then having magic done in the background
    attributes = {
        "record_bytes"           : re.compile(b"RECORD_BYTES *=.*\n?"),
        "image_ptr"              : re.compile(b"\^IMAGE *=.*\n?"),
        "filter_name"            : re.compile(b"FILTER_NAME *=.*\n?"),
        "exposure_duration"      : re.compile(b"EXPOSURE_DURATION *=(?:(?!\<).)*"),
        "lines"                  : re.compile(b"LINES *=.*\n?"),
        "line_samples"           : re.compile(b"LINE_SAMPLES *=.*\n?"),
        "sample_bits"            : re.compile(b"SAMPLE_BITS *=.*\n?"),
        "sample_type"            : re.compile(b"SAMPLE_TYPE *=.*\n?"),
        "derived_minimum"        : re.compile(b"DERIVED_MINIMUM *=.*\n?"),
        "derived_maximum"        : re.compile(b"DERIVED_MAXIMUM *=.*\n?"),
        "start_time"             : re.compile(b"START_TIME *=.*\n?"),
        "target_center_distance" : re.compile(b"TARGET_CENTER_DISTANCE *=(?:(?!\<).)*"),
    }

    bits_to_dtype = {
        ("LSB_UNSIGNED_INTEGER", 8) : np.uint8,
        ("LSB_UNSIGNED_INTEGER", 16): np.uint16,
        ("PC_REAL", 32)             : np.float32, 
    }

    def __init__(self, path):
        # these are my real attributes
        self.path = path
        self.metadata = {}
        self.image = None
        # these are attributes read from the file
        # -- these guys should come from the metaclass (TBD who knows when)
        self.record_bytes = 0
        self.image_ptr = 0
        self.filter_name = ""
        self.lines = 0
        self.line_samples = 0
        self.sample_bits = 0
        self.sample_type = ""
        self.derived_minimum = 0
        self.derived_maximum = 0
        self.buffer = b""
        self.parse()
    
    def __repr__(self):
        return "\n".join([
            f"< ImgParser object>",
            f"    {self.line_samples}x{self.lines} @ {self.sample_bits}",
            f"    {self.filter_name}",
            f"    dmax: {self.derived_maximum}, dmin: {self.derived_minimum}",
        ])
            

    def _read_attr(self, attr, data):
        rx = self.attributes[attr]
        list_attr = rx.findall(data)
        if not(list_attr):
            return False
        raw_attr = list_attr[0].strip()
        try:
            val = eval(raw_attr.rpartition(b"=")[2])
        except SyntaxError:
            val = raw_attr.rpartition(b"=")[2]
        self.__setattr__(attr, val)
        return True


    def parse(self):
        with open(self.path, "rb") as fd:
            data = fd.read(40960)  # this is a wild guess that should work
            for attr in self.attributes:
                self._read_attr(attr, data)
                #print(f"Reading {attr}...", end=" ")
                #if self._read_attr(attr, data):
                #    print("Found!")
                #else:
                #    print("Not found.")
            # if any of this attributes is missing, there's no furth
            if not(self.image_ptr * self.lines * self.line_samples * self.sample_bits):
                return None
            # now we're sure to have a valid image_ptr and the rest of the data
            fd.seek((self.image_ptr - 1) * self.record_bytes)
            size = self.lines * self.line_samples
            size *= (self.sample_bits // 8)
            #print(f"Want to read {size} bytes...", end="")
            self.buffer = fd.read(size)
            #print(f" could read {len(self.buffer)} bytes")

    def buffer_to_image(self):
        dtype = self.bits_to_dtype[(self.sample_type, self.sample_bits)]
        image = np.frombuffer(self.buffer, dtype=dtype)
        image = image.reshape(self.line_samples, self.lines)
        self.image = image            

# wondering if the VICAR parser should also stem from the same metaclass.
# maybe something that takes care of dynamic attributes and then the real
# classes below take care of how?
# or maybe a different metaclass altogether?
class VicarParser:
    def __init__(self, path):
        # these are my real attributes
        self.path = path
        self.metadata = {}
        self.image = None
        # these are attributes read from the file
        self.record_bytes = 0
        self.image_ptr = 0
        self.filter_name = ""
        self.lines = 0
        self.line_samples = 0
        self.sample_bits = 0
        self.sample_type = ""
        self.derived_minimum = 0
        self.derived_maximum = 0
        self.buffer = b""
        self.parse()
    
    def __repr__(self):
        return "\n".join([
            f"< VicarParser object>",
            f"    {self.line_samples}x{self.lines} @ {self.sample_bits}",
            f"    {self.filter_name}",
            f"    dmax: {self.derived_maximum}, dmin: {self.derived_minimum}",
        ])

    def parse(self):
        pass

    def buffer_to_image(self):
        pass

