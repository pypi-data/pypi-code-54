# Copyright 2015 SKA South Africa (http://ska.ac.za/)
# BSD license - see COPYING for details
"""Root of katportalclient package."""
from __future__ import absolute_import

from .client import (
    KATPortalClient, ScheduleBlockNotFoundError, SensorNotFoundError,
    SensorHistoryRequestError, ScheduleBlockTargetsParsingError,
    SubarrayNumberUnknown, SensorLookupError, InvalidResponseError,
    create_jwt_login_token, SensorSample, SensorSampleValueTime)
from .request import JSONRPCRequest


# Automatically added by katversion
__version__ = '0.1.dev8+user.mmphego.prepare.v0.2.2.ae16df6'

# Automatically added by katversion
__version__ = '0.1.dev10+master.ecb46e3'

# Automatically added by katversion
__version__ = '0.2.2'
