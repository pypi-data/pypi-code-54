
"""
File:
    yclip.py

Description:
    Clip data and replace values with flag.

Parameters:
    names: str/list of str
        List of pytplot names.
    ymin:
        Minimum value to clip
    ymax:
        Maximum value to clip
    flag:
        Values outside (ymin, ymax) are replaced with flag.
        Default is float('nan').
    new_names: str/list of str
        List of new_names for pytplot variables.
        If not given, then a suffix is applied.
    suffix:
        A suffix to apply. Default is '-clip'.
    overwrite:
        Replace the existing tplot name.

Notes:
    Allowed wildcards are ? for a single character, * from multiple characters.
    Similar to tclip in IDL SPEDAS.
    This function clips y-axis data. To clip time-axis, use time_clip.
"""

import pyspedas
import pytplot
import numpy as np


def yclip(names, ymin, ymax, flag=None, new_names=None, suffix=None,
          overwrite=None):

    old_names = pyspedas.tnames(names)

    if len(old_names) < 1:
        print('yclip error: No pytplot names were provided.')
        return

    if suffix is None:
        suffix = '-clip'

    if flag is None:
        flag = np.nan

    if overwrite is not None:
        n_names = old_names
    elif new_names is None:
        n_names = [s + suffix for s in old_names]
    else:
        n_names = new_names

    if isinstance(n_names, str):
        n_names = [n_names]

    if len(n_names) != len(old_names):
        n_names = [s + suffix for s in old_names]

    for i, old in enumerate(old_names):
        new = n_names[i]

        if new != old:
            pyspedas.tcopy(old, new)

        data = pytplot.data_quants[new].values
        try:
            for j, v in enumerate(data):
                try:
                    iterator = enumerate(v)
                except TypeError:
                    if not np.isnan(v) and (v <= ymin or v >= ymax):
                        data[j] = flag
                else:
                    for k, s in iterator:
                        if not np.isnan(s) and (s <= ymin or s >= ymax):
                            data[j][k] = flag

        except TypeError:  # data Not itterable
            print("Cannot clip data.")

        print('yclip was applied to: ' + new)
