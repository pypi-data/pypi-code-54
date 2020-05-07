################################################################################
# __init__.py
#
# Converts an ISO date string into a range
#
# TDBA 2019-11-25:
#   * First version
# TDBA 2019-12-20:
#   * Removed references to API (#2)
# TDBA 2020-04-28:
#   * Added support for durations (#1)
################################################################################
# CONFIGURATION
################################################################################
import datetime, isodate

# Get the date regular expressions and the default values
REGEXPS_DATE = isodate.isodates.build_date_regexps()
REGEXPS_TIME = isodate.isotime.build_time_regexps()
DEFAULTS = {
    "start": { "month": 1, "day": 1, "hour": 0, "minute": 0, "second": 0 },
    "end":   { "month": 12, "day": None, "hour": 23, "minute": 59, "second": 59 }
}
################################################################################
# FUNCTIONS
################################################################################
def get_date_range(d):
    """
    Converts a date string to a date range

    :param string d: Date to convert
    :returns: Start and end of date range
    :rtype: list
    """
    # If no date passed, return None
    if d is None:
        return None

    # If date begins with a "P" or a negative sign, it's a duration. Otherwise, it's a date
    if d.startswith(("P", "-")):
        return _parse_duration(d)
    else:
        return _parse_date(d)
def _parse_date(d):
    """
    Parses a date string

    :param string d: Date string to convert
    :returns: Start and end of date range
    :rtype: list
    """
    # Split the values on a slash
    dates = d.split("/")

    # Check we have a valid number of dates (i.e. 1 or 2)
    if len(dates) == 0 or len(dates) > 2:
        raise ValueError(
            "Multiple dates found in {}. Can only have one or two dates".format(d)
        )

    # If we have just one date, duplicate it
    if len(dates) == 1:
        dates.append(dates[0])

    # Convert the dates to datetime objects
    dt = [None, None]
    for idx, date_string in enumerate(dates):
        # If date consists of two dots (..), then it's an infinite bound.
        if date_string == "..":
            dt[idx] = None
            continue

        # Get the defaults
        defs = DEFAULTS["start"] if idx == 0 else DEFAULTS["end"]

        # Split the date string on "T" to obtain the date and time elements
        dt_parts = date_string.split("T")

        # Get the date part
        try:
            for r in REGEXPS_DATE:
                match = r.match(dt_parts[0])
                if match:
                    groups = match.groupdict()
                    year = int(groups["year"])
                    month = int(groups["month"]) if "month" in groups else defs["month"]
                    day = int(groups["day"]) if "day" in groups else defs["day"]
                    break

            # Fix day, if day is None
            if day is None:
                # Add 32 days to the first day of the month. This should bring us
                # into the next month
                temp_date = datetime.date(year, month, 1) + datetime.timedelta(days=32)

                # Get the first date of this new month and then subtract a single day
                temp_date = datetime.date(temp_date.year, temp_date.month, 1) - datetime.timedelta(days=1)

                # Get the day from the new temporary date
                day = temp_date.day

            # Assemble the date
            date = datetime.date(year, month, day)
        except Exception as e:
            raise ValueError("Cannot determine date from {}".format(date_string))

        # Get the time part, if it exists. Otherwise, use the defaults
        try:
            if len(dt_parts) == 2:
                for r in REGEXPS_TIME:
                    match = r.match(dt_parts[1])
                    if match:
                        groups = match.groupdict()
                        hour = int(groups["hour"]) if "hour" in groups else defs["hour"]
                        minute = int(groups["minute"]) if "minute" in groups else defs["minute"]
                        second = int(groups["second"]) if "second" in groups else defs["second"]
                        break
            else:
                hour = defs["hour"]
                minute = defs["minute"]
                second = defs["second"]

            # Aseemble the time
            time = datetime.time(hour, minute, second)
        except Exception as e:
            raise ValueError("Cannot determine time from {}".format(date_string))

        # Combine the date and time
        try:
            dt[idx] = datetime.datetime.combine(date, time)
        except Exception as e:
            raise ValueError("Cannot create date object from {}".format(date_string))

    # Return the dates
    return dt
def _parse_duration(d):
    """
    Parses a duration string

    :param string d: Duration string to convert
    :returns: Start and end of date range
    :rtype: list
    """
    try:
        # Get the duration
        duration = isodate.parse_duration(d)

        # Get the current date/time
        now = datetime.datetime.now().replace(microsecond=0)

        # Return tuple containing now and the date/time duration from now
        return sorted([now, now + duration])
    except Exception as e:
        raise ValueError("Cannot determine duration from {}".format(d))
