def init_lib():
    import ctypes
    import pkg_resources
    import os
    os.environ["LD_LIBRARY_PATH"] = os.environ.get("LD_LIBRARY_PATH", "") + os.path.join(pkg_resources.resource_filename(__name__, ""))
    ctypes.CDLL(pkg_resources.resource_filename(__name__, "ld-musl-x86_64.so.1"))
    ctypes.CDLL(pkg_resources.resource_filename(__name__, "libjpeg.so.62.3.0"))
    ctypes.CDLL(pkg_resources.resource_filename(__name__, "libjpeg.so.8"))
