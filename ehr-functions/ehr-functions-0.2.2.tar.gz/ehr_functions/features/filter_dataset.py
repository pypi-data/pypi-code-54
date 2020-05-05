import pandas as pd
import numpy as np



def tag_diagnosis_rows(df, name, codes):
    df[name] = 0
    df.loc[(df['Diagnosis1'].isin(codes)) | (df['Diagnosis2'].isin(codes)) | (df['Diagnosis3'].isin(codes)), name] = 1

    return df


# TODO - Use this in find_first
def get_patient_ids(df, codes, nth=None):
    return get_occurrence(df, codes, nth=nth)['PatientID'].unique().tolist()


def limit_df(df, patient_ids):
    return df[df['PatientID'].isin(patient_ids)]


def get_encounter_counts(df, df_filter=None):
    return __get_encounter_counts(df, df_filter)['num'].value_counts().sort_index()


def __get_encounter_counts(df, df_filter=None):
    if df_filter is None:
        df_use = df
    else:
        df_use = df[df_filter]

    # Get a small slice of the original dataframe
    unique_encounter_dates = df_use[['EncounterID', 'PatientID', 'EncounterDate']]

    # Drop duplicate dates for a specific patient
    unique_encounter_dates = unique_encounter_dates.drop_duplicates(['PatientID', 'EncounterDate'])

    # Get the number of encounters for each patient
    return unique_encounter_dates.groupby('PatientID').size().reset_index(name='num')


def limit_min_encounters(df, df_filter=None, min_enc=0):
    encounter_counts = __get_encounter_counts(df, df_filter=df_filter)

    encounter_counts = encounter_counts[encounter_counts['num'] >= min_enc]

    return df[df['PatientID'].isin(encounter_counts['PatientID'].unique())]


def drop_empty_encounters(df, columns_empty=None):
    if columns_empty is None:
        columns_empty = ['Diagnosis1', 'Diagnosis2', 'Diagnosis3', 'Procedure1', 'Procedure2', 'Procedure3']

    # Replace empty string with nan to allow for dropna to work
    df[columns_empty] = df[columns_empty].replace('', np.nan)

    # Drop na based off columns
    df = df.dropna(subset=columns_empty, how='all')

    # Convert back to empty string
    df[columns_empty] = df[columns_empty].replace(np.nan, '')

    return df


if __name__ == '__main__':
    FOLDER = 'interim/all/'
    FILE = 'dc_outpatient_encounters.feather'

    from ehr_functions.data.load_dataset import load_dataset

    a = load_dataset(FOLDER + FILE, num_patients=500)

    print('loaded dataset')

    from ehr_functions.features.code_descriptions import get_tbi

    tbi_codes = get_tbi()

    # a, a_tbi = find_first(a, 'TBI', tbi_codes)
    #
    # print('found first')
    #
    # a = limit_had_encounters(a)
    # print('limited encounters')

    from ehr_functions.features.code_descriptions import get_depression

    depression_codes = get_depression()

    ids = get_patient_ids(a, depression_codes, nth=2)

    print(ids)

    # a = tag_had_code(a, a, 'GotDepression', depression_codes)
