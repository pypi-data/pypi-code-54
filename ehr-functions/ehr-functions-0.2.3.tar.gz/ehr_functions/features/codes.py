from .. import files
import pandas as pd
import pkgutil
import io


def simplify(df, n=3, cols=None):
    if cols is None:
        cols = ['Diagnosis1', 'Diagnosis2', 'Diagnosis3']
        cols = [col for col in cols if col in df.columns]

    for col in cols:
        df[col] = df[col].str[:n]

    return df


def clean(df, cols=None):
    if cols is None:
        cols = ['Diagnosis1', 'Diagnosis2', 'Diagnosis3']
        cols = [col for col in cols if col in df.columns]

    for col in cols:
        df[col] = df[col].str.replace('.', '')
        df[col] = df[col].str.replace('_', '')
        df[col] = df[col].str.strip()
        df[col] = df[col].str.split(' ', n=0).str.get(0)

    return df


def __convert(df, cols, source, target):
    if cols is None:
        cols = ['Diagnosis1', 'Diagnosis2', 'Diagnosis3']
        cols = [col for col in cols if col in df.columns]

    table = pd.read_csv(io.BytesIO(pkgutil.get_data(__name__, '../files/icd9toicd10cmgem.csv')),
                        dtype={'icd9cm': str, 'icd10cm': str})
    table = table[[source, target]]
    table = table.set_index(source)
    mapping = table.to_dict()[target]

    unique_codes = set()
    for col in cols:
        unique_codes |= set(df[col].unique().tolist())
    unique_codes = list(unique_codes - set(mapping.keys()))

    for code in unique_codes:
        mapping[code] = code

    for col in cols:
        df[col] = df[col].map(mapping)

    return df


def convert_to_icd10(df, cols=None):
    return __convert(df, cols, 'icd9cm', 'icd10cm')


def convert_to_icd9(df, cols=None):
    return __convert(df, cols, 'icd10cm', 'icd9cm')


def get_ccs_mapping(name, level=None, code_type=10, data_type='dx'):
    if code_type == 10:
        table = pd.read_csv(io.BytesIO(pkgutil.get_data(__name__, '../files/ccs/icd10_' + data_type + '.csv')),
                            quotechar="'", dtype=str)
    elif code_type == 9:
        multi = '' if level is None else '_multi'
        table = pd.read_csv(io.BytesIO(pkgutil.get_data(__name__, '../files/ccs/icd9_' + data_type + multi + '.csv')),
                            quotechar="'", dtype=str)
        table['code'] = table['code'].str.strip()
        if 'single' in table.columns:
            table['single'] = table['single'].str.strip()
    else:
        raise ValueError('Invalid code_type specified: ' + str(code_type))

    if level is None:
        column = 'single'
    else:
        column = 'multi_' + str(level)
        if column not in table.columns:
            raise ValueError('Invalid level specified: ' + str(level))

    if not isinstance(name, list):
        table = table[table[column] == name]
        return table['code'].values.tolist()

    table = table[table[column].isin(name)]
    table = table[['code', column]]
    table = table.set_index('code')
    return table.to_dict()[column]
