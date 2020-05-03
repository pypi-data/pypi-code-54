class OVPNException(Exception):
    """Base exception for all that are raised by this lib"""

    pass


class OVPNTimeoutException(OVPNException):
    """Base exception for all that are related to timeouts"""

    pass


class OVPNStartupTimeoutException(OVPNTimeoutException):
    """Timeout during startup operation - OVPN not ready soon enough"""

    pass


class OVPNStopTimeoutException(OVPNTimeoutException):
    """Timeout during stop operation - OVPN still alive"""

    pass
