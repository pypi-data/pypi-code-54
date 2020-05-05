import pandas as pd


def get_nth_occurrence(df, codes, nth=None):
    if nth is None:
        nth = 0

    if not isinstance(codes, list):
        codes = [codes]

    df = df[['PatientID', 'EncounterDate', 'Diagnosis1', 'Diagnosis2', 'Diagnosis3']]
    df = df[(df['Diagnosis1'].isin(codes)) | (df['Diagnosis2'].isin(codes)) | (df['Diagnosis3'].isin(codes))]
    df = df.sort_values('EncounterDate')

    patients = df.groupby('PatientID')
    occurrence = patients.nth(nth)
    occurrence = occurrence.reset_index()

    return occurrence[['PatientID', 'EncounterDate']]


def tag_had_code(df, name, codes, nth=None):
    patient_id_list = get_nth_occurrence(df, codes, nth=nth)['PatientID'].unique().tolist()

    temp = pd.DataFrame({'PatientID': patient_id_list, name: True})
    df = df.merge(temp, on='PatientID', how='left', copy=False)
    df.loc[:, name] = df[name].fillna(False)

    return df


# TODO - unused
def __get_patients_had_encounters(df, days=365):
    df = df[['PatientID', 'TBIDays']]
    df = df[df['TBIDays'] >= days]
    return df['PatientID'].unique().tolist()
