
import datetime as dt
from math import ceil

import numpy as np
import pandas as pd
from scipy.signal import find_peaks, lfilter, butter, medfilt
from scipy.stats import entropy

from actigraph import raw_to_counts

# TODO?: convert Datetime->Float or vice versa to speed up computation

############################## Helper functions: ###############################

def median_filter(data, kernel_size=3):
    df_copy = data.copy()
    axes = [ax for ax in ['x','y','z','rx','ry','rz'] if ax in data.columns]
    for axis in axes:
        df_copy[axis] = medfilt(data[axis], kernel_size=kernel_size)
    return df_copy

def filt(accel, cutoff, btype, order=3):
    accel_copy = accel.copy()
    sr = get_sr(accel)
    nyq = 0.5 * sr
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype=btype, fs=sr)
    axes = [ax for ax in ['x','y','z','rx','ry','rz'] if ax in accel.columns]
    for axis in axes:
        accel_copy[axis] = lfilter(b, a, accel[axis])
    return accel_copy

def hpf(accel, cutoff, order=3):
    return filt(accel, cutoff, btype='highpass', order=order)

def lpf(accel, cutoff, order=3):
    return filt(accel, cutoff, btype='lowpass', order=order)

def bpf(accel, low=0.2, high=20, order=3):
    cutoff = np.array([low,high])
    return filt(accel, cutoff, btype='bandpass', order=order)

def get_starts_ends(data, epochs, window_size):
    # could use window+overlap instead of passing epochs.
    if type(data.index) == pd.DatetimeIndex:
        epoch_starts = epochs.index.to_pydatetime()
        epoch_ends = epoch_starts + dt.timedelta(seconds=window_size)
    elif type(data.index) == pd.Float64Index:
        epoch_starts = epochs.index.values
        epoch_ends = epoch_starts + window_size
    return epoch_starts, epoch_ends

def get_peaks_from_fft(yf, xf):
    """yf is the fft amplitude.  xf are the corresponding frequencies. returns
    (frequencies, heights)"""
    if len(yf) == 0:
        return [], []
    # Find peaks:
    prom = np.percentile(yf, 95)
    peaks, peak_props = find_peaks(yf, prominence=prom, height=(None,None))
    # Arrange by prominence:
    order = np.flip(np.argsort(peak_props['prominences']))
    freqs = xf[peaks[order]]
    heights = peak_props['prominences'][order]
    return freqs, heights

def get_sr(df):
    """Returns the sample rate in Hz for the given data.  May not work if SR isn't
    constant."""
    if len(df) < 2:
        raise ValueError("dataset must have >= 2 samples to find SR.")
    if type(df.index) == pd.DatetimeIndex:
        return 1/(df.index[1]-df.index[0]).total_seconds()
        # TODO: make a median method for this, rather than first 2 elements?
    elif type(df.index) == pd.Float64Index:
        #return 1/(df.index[1]-df.index[0])
        return 1.0/np.median(df.index.values[1:] - df.index.values[:-1])

def get_freq_stats(frame, **kwargs):
    """Find the most dominant frequencies (Hz) in VM acceleration between some start
    and stop times.  Peaks outside [fmin,fmax] are ignored.  The list is sorted
    by prominence.  Peak prominence must be >95th percentile of signal
    amplitudes to make the list.  Returns a dict containing freqs, peak heights,
    total power, power spectral entropy, f_625, and p_625.  If no peaks are
    found, peaks and heights are empty.

    Keyword arguments:
    frame -- a (slice of a) DataFrame
    sr    -- sample rate (Hz)
    fmin  -- minumum frequency to include (Hz)
    fmax  -- maximum frequency to include (Hz)
    """
    # TODO: pad data around frame to allow better FFT?
    if len(frame) < 2:
        return {
            'top_freqs': [],
            'top_freq_powers': [],
            'total_power': None,
            'entropy': None,
            'f_625': None,
            'p_625': None,
        }
    sr = kwargs.get('sr')
    if not sr:
        sr = get_sr(frame)
    fmin  = kwargs.get('fmin', 0.2)  # TODO: 0.1 default?
    fmax  = kwargs.get('fmax', 5)
    if (fmin > 0.6) or (fmax < 2.5):
        raise ValueError("[fmin, fmax] must include the range [0.6, 2.5] (Hz)")
    accel = frame.vm
    # Compute FFT:
    yf = np.abs(np.fft.rfft(accel))  # TODO?: might phase data be useful?
    xf = np.fft.rfftfreq( len(accel), 1.0/sr )
    freq_bin_width = xf[1]  # minus xf[0], which is 0
    # TODO?: 'friendly' window sizes for FFT performance
    # Crop to different frequency ranges:
    i625  = (xf > 0.6)  & (xf < 2.5)
    yf625 = yf[i625]
    xf625 = xf[i625]
    i     = (xf > fmin) & (xf < fmax)
    yf    = yf[i]
    xf    = xf[i]
    # TODO: adjust everything below to handle empty xf/yf
    # Find peaks:
    freqs, heights = get_peaks_from_fft(yf, xf)
    # Other stats:
    ent = entropy(yf**2)
    total_power = np.sum((yf/sr)**2) * freq_bin_width
    # total power is only within this restricted frequency range (0.2-5Hz;
    # reference uses 0.3-15Hz).  units are ~ W/kg not W.  to get total power
    # over all freqs, we don't need FFT, could just do np.sum(accel**2) / sr.
    try:
        peak_625_loc = np.argmax(yf625)
    except ValueError:
        peak_625_loc = None
    return {
        'top_freqs': freqs,
        'top_freq_powers': (heights/sr)**2 * freq_bin_width,
        'total_power': total_power,
        'entropy': ent,
        # TODO: use get_peaks_from_fft() for f_625+p_625 if there is a minimum
        # power requirement for them to be defined.
        'f_625': xf625[peak_625_loc] if peak_625_loc is not None else None,
        'p_625': (yf625[peak_625_loc]/sr)**2 * freq_bin_width if peak_625_loc is not None else None,
    }

######################### Feature-computing functions: #########################

def vm_accel(**kwargs):
    """kwargs:
       - data (the dataframe)
       - epochs
       - window_size
       - overlap
    """
    data = kwargs.get('data')
    if ('x' not in data.columns) and ('y' not in data.columns) and ('z' not in data.columns):
        return  # can't compute anything
    epochs = kwargs.get('epochs')
    window_size = kwargs.get('window_size')
    overlap = kwargs.get('overlap')
    if overlap == 0:
        if type(data.index) == pd.DatetimeIndex:
            groups = data.groupby(
                (data.index - data.index[0]).total_seconds() // window_size
            )
        elif type(data.index) == pd.Float64Index:
            groups = data.groupby(
                (data.index - data.index[0]) // window_size
            )
        means = groups.mean().vm.values
        stds  = groups.std().vm.values
        if len(means) == len(epochs):
            epochs['vm_mean'] = means
            epochs['vm_std']  = stds
        elif len(means) == len(epochs)+1:
            # off-by-one errors can happen if e.g. first sample is at time 0s
            # and last is at time 1200s.  that would result in e.g. 41 groups
            # to fill 40 windows.  we'll just delete the last group.
            # TODO: delete first OR last group, whichever had less samples
            # TODO?: fix that when creating epochs instead
            epochs['vm_mean'] = means[:len(epochs)]
            epochs['vm_std']  = stds[:len(epochs)]
        else:
            raise ValueError("Can't store %d results in %d windows." % (len(means), len(epochs)))
    else:
        # can't use groupby() etc. with overlapping windows.  see
        # https://github.com/pandas-dev/pandas/issues/15354.
        vm_mean = np.full(len(epochs), np.nan, dtype=np.float64)
        vm_std  = np.full(len(epochs), np.nan, dtype=np.float64)
        epoch_starts, epoch_ends = get_starts_ends(data, epochs, window_size)
        for i, (epoch_start, epoch_end) in enumerate(zip(epoch_starts, epoch_ends)):
            accel = data.loc[epoch_start:epoch_end]
            vm_mean[i] = np.mean(accel.vm)
            vm_std[i]  = np.std(accel.vm)
        epochs['vm_mean'] = vm_mean
        epochs['vm_std']  = vm_std

def timestamp_features(**kwargs):
    data = kwargs.get('data')
    if type(data.index) != pd.DatetimeIndex:
        return
    # TODO: compute hour of day, and day of week.  and maybe month or week of
    # year to capture season.  be sure to exclude (at least some of) these by
    # default in main code.
    raise NotImplementedError()

def freq_stats(**kwargs):
    """Gets dominant frequencies, power, entropy, etc."""
    data = kwargs.get('data')
    if ('x' not in data.columns) and ('y' not in data.columns) and ('z' not in data.columns):
        return  # can't compute anything
    epochs = kwargs.get('epochs')
    window_size = kwargs.get('window_size')
    epoch_starts, epoch_ends = get_starts_ends(data, epochs, window_size)
    f1          = np.full(len(epochs), np.nan, dtype=np.float64)
    p1          = np.full(len(epochs), np.nan, dtype=np.float64)
    f2          = np.full(len(epochs), np.nan, dtype=np.float64)
    p2          = np.full(len(epochs), np.nan, dtype=np.float64)
    f625        = np.full(len(epochs), np.nan, dtype=np.float64)
    p625        = np.full(len(epochs), np.nan, dtype=np.float64)
    total_power = np.full(len(epochs), np.nan, dtype=np.float64)
    ps_ent      = np.full(len(epochs), np.nan, dtype=np.float64)
    for i, (epoch_start, epoch_end) in enumerate(zip(epoch_starts, epoch_ends)):
        frame = data[epoch_start:epoch_end]
        results = get_freq_stats(frame, **kwargs)
        if len(results['top_freqs']) >= 1:
            f1[i] = results['top_freqs'][0]
            p1[i] = results['top_freq_powers'][0]
        if len(results['top_freqs']) >= 2:
            f2[i] = results['top_freqs'][1]
            p2[i] = results['top_freq_powers'][1]
        f625[i] = results['f_625']
        p625[i] = results['p_625']
        total_power[i] = results['total_power']
        ps_ent[i] = results['entropy']
        # Note: reference uses 0.3-15Hz total power.  We use 0.2-5Hz.
    f1_prev = np.concatenate(([np.nan],f1[:-1]))
    # TODO: standardize these (and all) output names:
    epochs['f1_Hz']       = f1
    epochs['f1_power']    = p1
    epochs['f1_change']   = f1 / f1_prev  # could do this in db instead, but meh.
    epochs['f2_Hz']       = f2
    epochs['f2_power']    = p2
    epochs['f625_Hz']     = f625
    epochs['f625_power']  = p625
    epochs['total_power'] = total_power
    epochs['p1_fraction'] = epochs['f1_power'] / epochs['total_power']
    epochs['ps_entropy']  = ps_ent

def corr_coeffs(**kwargs):
    data = kwargs.get('data')
    epochs = kwargs.get('epochs')
    window_size = kwargs.get('window_size')
    outputs = {}
    pairings = [['x','y'], ['x','z'], ['y','z'], ['rx','ry'], ['rx','rz'], ['ry','rz']]
    valid_pairs = [p for p in pairings if (p[0] in data.columns and p[1] in data.columns)]
    for pair in valid_pairs:
        pair_str = 'corr_' + pair[0]+pair[1]
        outputs[pair_str] = np.full(len(epochs), np.nan, dtype=np.float64)
    if len(outputs) == 0:
        return  # can't compute anything
    epoch_starts, epoch_ends = get_starts_ends(data, epochs, window_size)
    valid_axes = [ax for ax in ['x','y','z','rx','ry','rz'] if ax in data.columns]
    for i, (epoch_start, epoch_end) in enumerate(zip(epoch_starts, epoch_ends)):
        accel = data.loc[epoch_start:epoch_end]
        corrs = np.corrcoef(accel[valid_axes].T)
        for pair in valid_pairs:
            pair_str = 'corr_' + pair[0]+pair[1]
            if pair[0] in accel.columns and pair[1] in accel.columns:
                outputs[pair_str][i] = corrs[valid_axes.index(pair[0])][valid_axes.index(pair[1])]
    for col in outputs:
        epochs[col] = outputs[col]

def acti_counts(**kwargs):
    """Compute Actigraph-like "counts".  See
    https://www.ncbi.nlm.nih.gov/pubmed/28604558.

    See also:
    https://actigraph.desk.com/customer/en/portal/articles/2515835-what-is-the-difference-among-the-energy-expenditure-algorithms-
    https://actigraph.desk.com/customer/en/portal/articles/2515804-what-is-the-difference-among-the-met-algorithms-
    Maybe this if you have HR data:
    https://actigraph.desk.com/customer/en/portal/articles/2515579-what-is-hree-in-actilife-
    """
    data        = kwargs.get('data')
    if ('x' not in data.columns) and ('y' not in data.columns) and ('z' not in data.columns):
        return  # can't compute anything
    epochs      = kwargs.get('epochs')
    overlap     = kwargs.get('overlap')
    window_size = kwargs.get('window_size')
    sr          = kwargs.get('sr')
    if not sr:
        sr = get_sr(data)
    axis_counts = {}
    for axis in ['x','y','z']:
        if axis in data.columns:
            axis_counts[axis+'c'] = raw_to_counts(data[axis], sr)
    results = None
    for counts in axis_counts:
        if results is None:
            results = axis_counts[counts]**2
        else:
            results += axis_counts[counts]**2
    vmc = np.sqrt(results)
    # axis_counts and vmc contain the number of counts for each second of data.
    if type(data.index) == pd.DatetimeIndex:
        index = pd.date_range(
            freq = '1S',
            start = data.index[0] + dt.timedelta(seconds = 0.5),
            periods = len(vmc),
            name = 'time'
        )
    elif type(data.index) == pd.Float64Index:
        index = pd.Float64Index(
            data = np.arange(data.index[0]+0.5, data.index[-1]+0.5, 1),
            name = 'time'
        )
    if len(vmc) != len(index):
        rm_from_vmc = len(vmc) - len(index)
        if abs(rm_from_vmc) > 30:  # off by more than 30 seconds
            raise ValueError("Something is wrong.  Number of samples really doesn't match SR+timespan of recording.")
        print("Truncating %d second(s) of counts to (hopefully) match up with windows." % rm_from_vmc)
        if rm_from_vmc > 0:
            vmc = vmc[:len(index)]
        elif rm_from_vmc < 0:
            vmc = np.pad(vmc,(0,-rm_from_vmc),mode='constant',constant_values=np.nan)
    counts = pd.Series(
        data = vmc,
        index = index,
        dtype = np.float64,
        name = 'counts_per_sec'
    )
    # note: with 0.5s offset, counts happen *around* reported time, not just
    # before or after it
    if overlap == 0:
        counts = counts.to_frame()
        counts['elapsed_sec'] = counts.index - data.index[0]
        if type(data.index) == pd.DatetimeIndex:
            counts['elapsed_sec'] = counts['elapsed_sec'].total_seconds()
        counts_groups = counts.groupby(counts.elapsed_sec // window_size).counts_per_sec
        epochs['cpm_mean'] = counts_groups.sum().values / (window_size/60.0)
    else:
        cpm_mean = np.full(len(epochs), np.nan, dtype=np.float64)
        epoch_starts, epoch_ends = get_starts_ends(data, epochs, window_size)
        for i, (epoch_start, epoch_end) in enumerate(zip(epoch_starts, epoch_ends)):
            accel = data.loc[epoch_start:epoch_end]
            cpm_mean[i] = np.sum(counts[epoch_start:epoch_end]) / (window_size/60.0)
        epochs['cpm_mean'] = cpm_mean

################# Map functions to the features they compute: ##################

function_feature_map = {

    vm_accel:           ['vm_mean', 'vm_std'],

    freq_stats:         ['f1_Hz', 'f1_power', 'f1_change', 'f2_Hz', 'f2_power',
                         'f625_Hz', 'f625_power', 'total_power', 'p1_fraction',
                         'ps_entropy'],

    corr_coeffs:        ['corr_xy', 'corr_xz', 'corr_yz',
                         'corr_rxry', 'corr_rxrz', 'corr_ryrz'],

    acti_counts:        ['cpm_mean'],

    timestamp_features: [],  # TODO

}

################################################################################
