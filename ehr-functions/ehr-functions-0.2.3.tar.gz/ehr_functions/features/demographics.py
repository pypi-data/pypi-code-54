from ehr_functions.utils import make_numeric


def get_features(df, cols=None):
    if cols is None:
        cols = ['PatientAge', 'PatientGender', 'PatientCategory']
        cols = [col for col in cols if col in df.columns]

    # Drop duplicates based off PatientID
    df = df.drop_duplicates('PatientID', keep='first')

    # Select demographics and patient id
    df = df[['PatientID'] + cols]

    # Convert columns that are not numbers and more than two categories into separate columns
    df = make_numeric(df, cols=cols)

    return df
