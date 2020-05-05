import pandas as pd


def __count_clinics(df, groups):
    return df.groupby('PatientID')[groups].sum().reset_index()


def count_clinics(df, groups, windows, prior=False):
    """

    :param df:
    :param groups:
    :param windows:
    :param prior:
    :return:
    """
    if windows is None:
        raise ValueError('Windows cannot be None.')

    if not isinstance(windows[0], list):
        windows = [windows]

    if prior:
        for w, window in enumerate(windows):
            temp = window[0]
            windows[w][0] = window[1] * -1
            windows[w][1] = temp * -1

    counts = None
    for window in windows:
        df_window = df[(df['TBIDays'] >= window[0]) & (df['TBIDays'] < window[1])]
        counts_window = __count_clinics(df_window, groups)
        col_map = {}
        for col in counts_window.columns:
            if col != 'PatientID':
                col_map[col] = col + '_' + str(window[0]) + ',' + str(window[1]) + ''

        counts_window = counts_window.rename(index=str, columns=col_map)
        if counts is None:
            counts = counts_window
        else:
            counts = pd.merge(counts, counts_window, on='PatientID', how='outer')

    return counts
