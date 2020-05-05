from ehr_functions.paths import DATA
import pandas as pd
import json
import os


def get_depression():
    """
    Source: http://icd10cmcode.com/what-is-the-icd-10-for-depression.php
    :return:
    """
    depression_codes = ['F0390', 'F341', 'F4321', 'F0631', 'F0632' 'F251']
    for i in range(10):
        depression_codes.append('F32' + str(i))

    for i in range(10):
        depression_codes.append('F33' + str(i))

    return depression_codes


def get_depression_dod():
    with open(os.path.join(DATA, 'external/health-mil-codes/depressive.json')) as f:
        data = json.load(f)

    return data['icd9'] + data['icd10']


# These are actually MOOD DISORDERS
# CCS for ICD-10 removed the sub level for depression
def get_depression_ccs():
    with open(os.path.join(DATA, 'external/r-icd/json/icd9_map_multi_ccs.json')) as f:
        data9 = json.load(f)

    with open(os.path.join(DATA, 'external/r-icd/json/icd10_map_ccs.json')) as f:
        data10 = json.load(f)

    return data9['lvl2']['5.8'] + data10['lvl2']['5.8']


def get_tbi_dod(mild=False):
    file = os.path.join(DATA,
                        'external/health-mil-codes/FINAL_TBI_cd_Appendix II_TBI ICD9_ICD10 Code Sets Excel_APR16.xlsx')

    df9 = pd.read_excel(file, sheet_name='TBI_ICD9', dtype=str)
    df10 = pd.read_excel(file, sheet_name='TBI_ICD10', dtype=str)

    # Stripping spaces from ends of strings (unsure why they are there)
    df9 = df9.apply(lambda x: x.str.strip())
    df10 = df10.apply(lambda x: x.str.strip())

    if mild:
        df9 = df9[df9['Severity Classification'] == 'Mild']
        df10 = df10[df10['Severity Classification'] == 'Mild']

    codes = df9['ICD9'].tolist() + df10['ICD10'].tolist()
    return codes


def get_tbi(mild=False):
    tbi_codes = pd.read_csv(os.path.join(DATA, 'raw/TBI_ICD_CODE_LIST.csv'))
    if mild:
        tbi_codes = tbi_codes[tbi_codes['SEVERITY'] == 'Mild']
    return tbi_codes['ICD'].tolist()
