import time
from pythonjsonlogger import jsonlogger


class JsonTimezoneFormatter(jsonlogger.JsonFormatter):
    tz_format = "%z"
    default_msec_tz_format = '%s,%03d %s'

    def formatTime(self, record, datefmt=None):  # noqa
        ct = self.converter(record.created)
        t = time.strftime(self.default_time_format, ct)
        tz = time.strftime(self.tz_format, ct)
        s = self.default_msec_tz_format % (t, record.msecs, tz)
        return s
