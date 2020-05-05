from ehr_functions.paths import DATA_EXTERNAL
import pandas as pd
import json
import os


def get_ccs_mapping(multi=False, level=1):
    icd9_file = 'icd9_map_single_ccs.json' if not multi else 'icd9_map_multi_ccs.json'
    with open(os.path.join(DATA_EXTERNAL, 'r-icd', 'json', icd9_file)) as f:
        mapping = json.load(f)
        if multi:
            mapping = mapping['lvl' + str(level)]

    with open(os.path.join(DATA_EXTERNAL, 'r-icd', 'json', 'icd10_map_ccs.json')) as f:
        mapping_10 = json.load(f)
        level_list = ['single'] if not multi else ['lvl' + str(level)]
        for level in level_list:
            for key, val in mapping_10[level].items():
                if key not in mapping:
                    mapping[key] = []

                mapping[key] += val

    return mapping


def convert_mapping(df, mapping):
    inverse_mapping = {v: k for k, values in mapping.items() for v in values}

    for d in range(1, 4):  # 1, 2, 3
        diagnosis = 'Diagnosis' + str(d)
        diagnosis_map = diagnosis + '_Map'
        df[diagnosis_map] = df[diagnosis].map(inverse_mapping)
        df.loc[df[diagnosis_map].isna(), diagnosis_map] = df[df[diagnosis_map].isna()][diagnosis]

    return df


def count_symptom_windows(df, symptom=None, windows=None):
    if not isinstance(windows[0], list):
        windows = [windows]

    df = df[df['Symptom_' + symptom] > 0]

    counts = None
    for window in windows:
        df_window = df[(df['TBIDays'] >= window[0]) & (df['TBIDays'] < window[1])]
        col_name = 'Symptom_' + symptom + '_' + str(window[0]) + '_' + str(window[1])
        df_window = df_window.groupby('PatientID')['Symptom_' + symptom].sum().reset_index(name=col_name)
        if counts is None:
            counts = df_window
        else:
            counts = pd.merge(counts, df_window, on='PatientID', how='outer')

    counts = counts.fillna(0)

    return counts


def __count_groups(df, groups, diagnoses=None):
    if diagnoses is None:
        diagnoses = range(1, 4)  # 1, 2, 3
    elif not isinstance(diagnoses, list):
        diagnoses = [diagnoses]

    df_filter = True
    for d in diagnoses:
        df_filter = df_filter | (df['Diagnosis' + str(d) + '_Map'].isin(groups))

    df = df[df_filter]

    counts = None
    for group in groups:
        df_grp = df[(df['Diagnosis1_Map'] == group) | (df['Diagnosis3_Map'] == group) | (df['Diagnosis3_Map'] == group)]
        df_grp = df_grp.groupby('PatientID').size().reset_index(name=group + '_Count')
        if counts is None:
            counts = df_grp
        else:
            counts = pd.merge(counts, df_grp, on='PatientID', how='outer')

    counts = counts.fillna(0)

    return counts


def count_groups(df, groups, diagnoses=None, windows=None, prior=False):
    if windows is None:
        raise ValueError('Windows cannot be None anymore.')
        windows = [[0, 365]]

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
        counts_window = __count_groups(df_window, groups, diagnoses=diagnoses)
        if counts is None:
            counts = counts_window
        else:
            counts = pd.merge(counts, counts_window, on='PatientID', how='outer')

    return counts
