
import datetime as dt
from math import ceil
from warnings import warn

import pandas as pd
import numpy as np

from .features import function_feature_map, get_sr, lpf, median_filter

#################################### Class: ####################################

class AFE:
    """Accelerometer Feature Extractor.  Extracts features useful for machine
    learning from raw accelerometer/gyroscope data."""

    def __init__(self, data, sr=None, interpolate=True, warn_interpolating=True, smooth=True):
        """data is a pandas DataFrame containing a time-based index (either timestamp,
        or seconds elapsed).  Columns must be labeled x, y, z (for
        accelerometer) and rx, ry, rz (for gyroscope).  Units must be g's.  Any
        columns may be omitted, e.g. a 2-axis accelerometer may include only x and
        y.  You shouldn't normally need to specify sample rate (sr).

        If interpolate is set and the sample rate seems inconsistent within the
        data, we'll interpolate the data to a fixed sample rate (matching the
        intended original SR as best we can).

        This class will store a copy of the original DataFrame.
        """
        if type(data) != pd.DataFrame:
            raise TypeError("data must be a Pandas DataFrame.")
        data = data.copy()  # never mess with the original
        check_timeindex(data)
        check_axes(data)
        data.sort_index(inplace=True)  # this really shouldn't be necessary...
        if not sr:
            sr = get_sr(data)
        new_df = interpolate_data(data, sr=sr, warn_interpolating=warn_interpolating)
        if new_df is not None:
            data = new_df
        # TODO?: unit conversion
        self.data = data
        self.sr = sr
        self.data_is_smoothed = False
        if smooth:
            self.smooth_data()

    def smooth_data(self):
        data = median_filter(self.data)
        data = lpf(data, cutoff=0.5*self.sr, order=3)
        self.data = data
        self.data_is_smoothed = True

    def compute_vm_accel(self, overwrite=False):
        if 'vm' not in self.data.columns or overwrite:
            vm = np.zeros(len(self.data))
            for axis in ['x','y','z']:
                if axis in self.data.columns:
                    vm = vm + self.data[axis].values**2
            self.data['vm'] = np.sqrt(vm.astype(np.float64))

    def get_features(self, window_size=30, overlap=0, include_timestamp_features=False,
                     include_features=[], exclude_features=[]):
        """Get a DataFrame of features.  Data will be segmented into window_size-second
        windows with overlap-second overlaps.  Set window_size and overlap to
        None to extract 1 set of features for the entire dataset.

        If include_timestamp_features is True, and the dataset has a timestamp
        index, features such as day_of_week will be included in the returned
        DataFrame.  This may be useful to make predictions that have seasonal,
        circadian, or other time-dependence.

        include_features and exclude_features are whitelist/blacklist (list of
        strings) of features to be computed.  If a feature extraction function
        provides some features that are not blacklisted, but some that are, it
        will be run anyway, and the blacklisted features will be dropped after
        computing them.
        """
        # TODO: implement some kind of save/don't-recompute option that
        # preserves already-computed features internally and can recall them
        # without recomputing.

        if overlap >= window_size:
            raise ValueError("overlap must be less than window size.")

        # TODO: support negative overlap to allow gaps (if it doesn't work already)

        if include_features:
            functions_to_run = [fn for fn in function_feature_map if not set(function_feature_map[fn]).isdisjoint(set(include_features))]
        else:
            functions_to_run = list(function_feature_map.keys())
        if exclude_features:
            functions_to_run = [fn for fn in functions_to_run if not set(function_feature_map[fn]).issubset(set(exclude_features))]

        start_times = get_epoch_start_times(self.data, window_size, overlap)
        epochs = pd.DataFrame(data=None, index=start_times,
                              columns=None, dtype=None)

        # could store one of these instead of passing window and overlap around separately from epochs:
        # epochs.window_size = window_size
        # epochs.window_overlap = overlap


        # TODO?: remove gravity (or split from 'body' accel)?  e.g. "low pass
        # Butterworth filter with a corner frequency of 0.3 Hz".  some other
        # papers suggest 0.25-0.5 Hz cutoff.


        self.compute_vm_accel()
        for function in functions_to_run:
            function(
                data = self.data,
                epochs = epochs,  # function will modify this in place.  at least that's the plan right now.
                window_size = window_size,
                overlap = overlap,
                include_timestamp_features = include_timestamp_features,
                sr = self.sr,
            )
        epochs = epochs[[col for col in epochs.columns if col not in exclude_features]]
        return epochs

############################## Helper functions: ###############################

def check_timeindex(df):
    """Make sure the DataFrame's index is either float or timestamp.
    """
    if type(df.index) == pd.DatetimeIndex or type(df.index) == pd.Float64Index:
        return
    raise TypeError("data index must be float or timestamp.")

def check_axes(df):
    needed = ['x','y','z','rx','ry','rz']
    if set(df.columns).isdisjoint(needed):
        raise ValueError("data must contain some columns from [x,y,z,rx,ry,rz].")

def get_epoch_start_times(data, window_size, overlap):
    """Get the start times for all epochs in this recording (as a pandas Index)."""
    period = window_size - overlap
    if type(data.index) == pd.DatetimeIndex:
        start_times = pd.date_range( start = data.index[0],
                                     end   = data.index[-1],
                                     freq  = '%dS'%period,
                                     name  = 'epoch_start' )
    elif type(data.index) == pd.Float64Index:
        timespan = data.index[-1] - data.index[0]
        windows = ceil(timespan / window_size)
        start_times = [data.index[0] + i*period for i in range(windows)]
        start_times = pd.Float64Index(start_times, name = 'epoch_start')
    return start_times

def interpolate_data(df, **kwargs):
    """Returns a new DataFrame with interpolated copies of the original data.
    Returns None if interpolation wasn't needed."""
    sr = kwargs.get('sr')
    warn_interpolating = kwargs.get('warn_interpolating')
    timespan = df.index[-1] - df.index[0]
    if type(df.index) == pd.DatetimeIndex:
        timespan = timespan.total_seconds()
    apparent_timespan = len(df)/sr
    if ceil(timespan) == ceil(apparent_timespan):
        return None  # seems good enough as-is
    # based on number of rows in df, we have apparent_timespan seconds of data.
    # but based on first and last timestamp, we have a different amount of data.
    # so we'll interpolate df to fix the inconsistent SR.
    if warn_interpolating:
        warn("Sample rate doesn't seem consistent.  Will interpolate data.")
    step = 1/sr
    if type(df.index) == pd.DatetimeIndex:
        step = dt.timedelta(seconds=step)
    new_t = np.arange(df.index.values[0], df.index.values[-1], step)
    keep_cols = ['x','y','z','rx','ry','rz']
    new_df = pd.DataFrame(
        index = new_t,
        columns = keep_cols,
    )
    for axis in keep_cols:
        if axis in df.columns:
            col_interped = np.interp(new_t, df.index.values, df[axis].values)
            new_df[axis] = col_interped
        else:
            new_df.drop(columns=axis, inplace=True)
    return new_df

################################################################################
