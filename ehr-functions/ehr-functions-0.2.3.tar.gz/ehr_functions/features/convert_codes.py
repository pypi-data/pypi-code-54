from ehr_functions.paths import ICD_MAPPINGS
import json
import os


def convert_codes_ccs_mapping(df, cols):
    if not isinstance(cols, list):
        cols = [cols]

    with open(os.path.join(ICD_MAPPINGS, 'icd10_map_ccs.json')) as f:
        mapping = json.load(f)
        mapping = mapping['lvl1']

    fast_mapping = {code: k for k, v in mapping.items() for code in v}

    def fast_convert(code):
        if code == '':
            return code

        if code.startswith('DOD'):
            if code.startswith('DOD02'):
                return 'DOD02'
            elif code.startswith('DOD03'):
                return 'DOD03'
            else:
                return code

        if code == 'NoDx':
            return ''

        if code in fast_mapping:
            return fast_mapping[code]

        keys = [key for key in fast_mapping.keys() if key.startswith(code)]

        if len(keys) > 0:
            return fast_mapping[keys[0]]

        raise Exception('Unable to find code ' + code)

    for col in cols:
        df.loc[:, col] = df[col].apply(fast_convert)

    return df
