from collections import defaultdict
from crdatamgt.formulations import formulation_write
from crdatamgt.helpers import workbook_load_path, data_extraction, rename_dictionary
import pandas as pd

def load_topic(path):
    print(path)
    wb = workbook_load_path(path)
    return wb


def read_topic(wb, formulation_path):
    df_dictionary = defaultdict()
    for sheet in wb.sheetnames:
        df_dictionary[sheet] = data_extraction(wb, sheet)
    if 'Formulation' in df_dictionary.keys():
        test = df_dictionary['Formulation']['Test'].drop_duplicates().dropna()
        if test.isin(['Henry']).any():
            df_dictionary['Formulation Group'] = formulation_group(df_dictionary['Formulation'])
        df_dictionary['Formulation'] = formulation_write(df_dictionary.get('Formulation'), formulation_path)

    if 'Results' in df_dictionary.keys():
        if 'Replicate' in df_dictionary['Results']:
            df_dictionary['Results'] = pd.DataFrame(
                df_dictionary['Results'].set_index('Replicate').mean().round(2)).transpose().add_suffix(' Average')

    return df_dictionary


def formulation_group(formulas):
    temp_formulation_group = []
    result = formulas.drop(columns='Formulation').mean().round(0)
    fc = pd.DataFrame(result[result > 5]).transpose()
    fc.columns = map(str.lower, fc.columns)
    fc.rename(columns=rename_dictionary(), inplace=True)
    for item in fc:
        temp_formulation_group.append(f"{item} {fc[item].values[0]}")
    fg = ' '.join(temp_formulation_group)
    return pd.DataFrame(columns=['Formulation Group'], data=[fg])


def update_formulations(formulation_frame):
    return formulation_write(formulation_frame)
