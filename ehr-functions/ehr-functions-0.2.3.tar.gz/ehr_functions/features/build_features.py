def build_static(df, x_col, y_col):
    if not isinstance(x_col, list):
        x_col = [x_col]

    df = df[x_col + [y_col] + ['PatientID']]
    df = df.drop_duplicates('PatientID', keep='first')

    x = df[x_col].values
    y = df[y_col].tolist()

    return x, y


def group_codes(df, col, groups):
    for group in groups:
        df[col + '_' + group['title']] = df[col].apply(lambda x: True if x == value else False)
    # Diagnosis1, Diagnosis2, Diagnosis3
    # Procedure1, Procedure2, Procedure3
    pass


def get_xy(features, df, predictor):
    df = df.drop_duplicates(['PatientID', predictor])
    features = features.merge(df[['PatientID', predictor]], on='PatientID', how='left')

    y = features[['PatientID', predictor]]
    y = y[predictor].tolist()

    x = features.drop(columns=['PatientID', predictor])
    x = x.values

    return x, y
