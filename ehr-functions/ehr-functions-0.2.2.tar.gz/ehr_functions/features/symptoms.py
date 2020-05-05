import pandas as pd


def add_symptom_columns(df, symptom_mapping, columns=None):
    if columns is None:
        columns = ['Diagnosis1', 'Diagnosis2', 'Diagnosis3']

    inv_mapping = {v: k for k, values in symptom_mapping.items() for v in values}

    columns_new = []
    for col in columns:
        df[col + '_Symptom'] = df[col].map(inv_mapping)
        columns_new.append(col + '_Symptom')

    df = pd.get_dummies(df, columns=columns_new)
    symptom_columns = []
    for key in symptom_mapping.keys():
        df['Symptom_' + key] = 0
        symptom_columns.append('Symptom_' + key)
        for col in columns_new:
            if col + '_' + key in df.columns:
                df['Symptom_' + key] = df['Symptom_' + key] + df[col + '_' + key]
                df = df.drop(columns=[col + '_' + key], axis=1)

    return df, symptom_columns
