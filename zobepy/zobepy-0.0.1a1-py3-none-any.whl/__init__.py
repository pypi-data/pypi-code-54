"""zobepy - zobe's unsorted library.

This is an unsorted library, so some of functions or classes
may move to separate packages in the future.

Shortnames
==========

You may use short names instead of poor long names.

.. csv-table::
    :header: Short Name, Long Name
    :widths: 5, 5

    zobepy.EyeFriendlyBytes, zobepy.eye_friendly.EyeFriendlyBytes
    zobepy.SubProcess, zobepy.subpr.SubProcess

"""

__version_info__ = ('0', '0', '1a1')
__version__ = '.'.join(__version_info__)

from .eye_friendly import EyeFriendlyBytes
from .subpr import SubProcess
import zobepy.dump
