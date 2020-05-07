from datetime import datetime as dt, timedelta
import pytz

eastern = pytz.timezone('US/Eastern')
utc = pytz.utc


def dt_to_timestamp(datetime_obj, ts_form):
    return datetime_obj.strftime(ts_form)


def dt_set_eastern(datetime_obj):
    return eastern.localize(datetime_obj)


def dt_to_utc(utc_datetime_obj):
    return utc_datetime_obj.astimezone(tz=utc)


def dt_utc_now(seconds_delta=0):
    return dt.utcnow() - timedelta(seconds=seconds_delta)


def elq_time_str_to_datetime(timestamp):
    """
    Convert either the BULK or REST-formatted timestamps from Eloqua to a standardized datetime object
    :param timestamp: the timestamp as received from Eloqua's API record instance
    :type timestamp: str
    :return: datetime object (no timezone specified on object, but is in eastern time)
    :rtype: str
    """
    try:
        return dt.strptime(timestamp, '%m/%d/%Y %H:%M:%S %p')
    except ValueError:
        return dt.strptime(timestamp[:-4], '%Y-%m-%d %H:%M:%S')


def elq_est_timestamp_to_utc_timestamp(eloqua_str_ts, ts_form='%Y-%m-%d %H:%M:%S'):
    """
    Eloqua has all their timestamps as EST (at least when using v1 of their REST API). To keep our times consistent,
    we want to convert EST to UTC for our logging purposes.
    :param eloqua_epoch: an eloqua epoch in EST
    :type eloqua_epoch: str
    :param ts_form: a datetime strftime output format to use
    :type ts_form: str
    :return: a timestamp in UTC formatted as 'ts_form'
    :rtype: str
    """
    if eloqua_str_ts:
        return dt_to_timestamp(dt_to_utc(dt_set_eastern(elq_time_str_to_datetime(eloqua_str_ts))), ts_form)
    else:
        return dt_to_timestamp(dt_utc_now(), ts_form)