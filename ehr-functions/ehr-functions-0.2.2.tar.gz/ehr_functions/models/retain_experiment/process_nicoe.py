import os
import time

from ehr_functions.data.load_dataset import load_dataset, load_mapping
from ehr_functions.features.symptoms import add_symptom_columns
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from ehr_functions.paths import DATA

FOLDER = 'interim/acute_chronic/'
MIN_DAYS = 14


def compute_outcome(df, df_tbi):
    symptom_mapping = load_mapping('interim/acute_chronic/symptom_mapping.json', json_file=True)
    symptom_mapping['MentalHealth'] = symptom_mapping['Anxiety'] + symptom_mapping['Depression'] + symptom_mapping[
        'Psychology'] + symptom_mapping['PTSD']
    del symptom_mapping['Anxiety']
    del symptom_mapping['Depression']
    del symptom_mapping['Psychology']
    del symptom_mapping['PTSD']

    df, symptom_columns = add_symptom_columns(df, symptom_mapping)

    outcome = df[df['TBIDays'] > MIN_DAYS].groupby('PatientID')['Symptom_MentalHealth'].sum().reset_index()
    outcome = outcome.rename(index=str, columns={'Symptom_MentalHealth': 'Outcome_MentalHealth'})

    outcome_column = 'Outcome_MentalHealth'
    outcome[outcome_column] = outcome[outcome_column].astype(bool).astype(int)
    outcome = pd.merge(outcome, df_tbi[['PatientID']], on='PatientID', how='outer')
    outcome[outcome_column] = outcome[outcome_column].fillna(0)

    print('outcome.value_counts()', outcome[outcome_column].value_counts())
    all_targets = pd.DataFrame(data={'target': outcome[outcome_column].values}
                               , columns=['target'])

    target_train, target_test = train_test_split(all_targets, train_size=0.7, random_state=12345)

    return target_train, target_test


def get_unique_diagnoses(df, display=True):
    unique_diagnoses = df['Diagnosis1'].unique().tolist() + df['Diagnosis2'].unique().tolist()
    unique_diagnoses += df['Diagnosis3'].unique().tolist()

    unique_diagnoses = list(set(unique_diagnoses))
    unique_diagnoses.remove('')
    if display:
        print('Num Unique Diagnoses', len(unique_diagnoses))

    return unique_diagnoses


def convert_diagnoses(df):
    # df['Diagnosis1'] = df['Diagnosis1'].str[:3]
    # df['Diagnosis2'] = df['Diagnosis2'].str[:3]
    # df['Diagnosis3'] = df['Diagnosis3'].str[:3]

    unique_diagnoses = get_unique_diagnoses(df)

    diagnosis_mapping = {code: i for i, code in enumerate(unique_diagnoses)}
    diagnosis_mapping[''] = np.nan
    df['Diagnosis1'] = df['Diagnosis1'].map(diagnosis_mapping)
    df['Diagnosis2'] = df['Diagnosis2'].map(diagnosis_mapping)
    df['Diagnosis3'] = df['Diagnosis3'].map(diagnosis_mapping)

    return df


def map_diagnoses(df):
    from ehr_functions.features.code_groups import get_ccs_mapping
    ccs_mapping = get_ccs_mapping(multi=False)
    inv_mapping = {code: i for i, (k, codes) in enumerate(ccs_mapping.items()) for code in codes}

    # all_diag = np.unique(df[['Diagnosis1', 'Diagnosis2', 'Diagnosis3']].values.ravel('K'))
    # diag_mapping = {code: index for index, code in enumerate(all_diag)}

    df['Diagnosis1'] = df['Diagnosis1'].map(inv_mapping)
    df['Diagnosis2'] = df['Diagnosis2'].map(inv_mapping)
    df['Diagnosis3'] = df['Diagnosis3'].map(inv_mapping)

    print('max diagnosis', df[['Diagnosis1', 'Diagnosis2', 'Diagnosis3']].max())

    return df


def __patient_codes(patient):
    blah = patient[['Diagnosis1', 'Diagnosis2', 'Diagnosis3']].dropna(how='all').values
    blah = [[code for code in encounter if ~np.isnan(code)] for encounter in blah]
    return blah


def __patient_days(patient):
    return patient[['TBIDays']].values


def __patient_info(patient):
    return patient[['PatientAge']].values


def create_input_old(df):
    patient_seqs = []
    patient_to_event = []
    patient_numerics = []
    df = df[(df['TBIDays'] >= -365) & (df['TBIDays'] <= MIN_DAYS)]

    for patient_id, patient in df.groupby('PatientID'):
        current_seq = []
        current_to_event = []
        current_numerics = []
        for day, rows in patient.groupby('TBIDays'):
            codes = np.unique(rows[['Diagnosis1', 'Diagnosis2', 'Diagnosis3']].values.ravel('K'))
            current_seq.append(codes)
            current_to_event.append(day)
            current_numerics.append(day)

        patient_seqs.append(current_seq)
        patient_to_event.append(current_to_event)
        patient_numerics.append(current_numerics)

    all_data = pd.DataFrame(data={'codes': patient_seqs,
                                  'to_event': patient_to_event,
                                  'numerics': patient_numerics}
                            , columns=['codes', 'to_event', 'numerics'])

    data_train, data_test = train_test_split(all_data, train_size=0.7, random_state=12345)
    return data_train, data_test


def create_input(df):
    patient_seqs = df.groupby('PatientID').apply(__patient_codes).reset_index()[0].values
    patient_to_event = df.groupby('PatientID').apply(__patient_days).reset_index()[0].values
    patient_numerics = df.groupby('PatientID').apply(__patient_info).reset_index()[0].values

    all_data = pd.DataFrame(data={'codes': patient_seqs,
                                  'to_event': patient_to_event,
                                  'numerics': patient_numerics}
                            , columns=['codes', 'to_event', 'numerics'])

    data_train, data_test = train_test_split(all_data, train_size=0.7, random_state=12345)
    return data_train, data_test


def create_data(num_patients=None, ccs=False, data_type=None):
    # start_time = time.time()
    df_tbi = load_mapping(FOLDER + 'patient_list')
    if data_type == 'train':
        df_tbi = df_tbi[df_tbi['Type'] == 'train']

    if num_patients is not None:
        df_tbi = df_tbi[:num_patients]
    df = load_dataset(FOLDER + 'dc_outpatient.feather')
    df = df[df['PatientID'].isin(df_tbi['PatientID'].unique())]
    df = df[df['PatientID'].isin(df[(df['TBIDays'] >= -365) & (df['TBIDays'] <= MIN_DAYS)]['PatientID'].unique())]
    df = df.reset_index(drop=True)
    df_tbi = df_tbi.reset_index(drop=True)
    # df[['Diagnosis1', 'Diagnosis2', 'Diagnosis3']] = df[['Diagnosis1', 'Diagnosis2', 'Diagnosis3']].replace(0, np.nan)
    # df = df.dropna(how='all', subset=['Diagnosis1', 'Diagnosis2', 'Diagnosis3'])
    df = df.sort_values(by=['PatientID', 'TBIDays'], ascending=[True, True])
    df_tbi = df_tbi.sort_values(by='PatientID', ascending=True)
    y_train, y_test = compute_outcome(df, df_tbi)

    # Next going to compute feature vectors
    df = df[(df['TBIDays'] >= -365) & (df['TBIDays'] <= MIN_DAYS)]
    if ccs:
        df = map_diagnoses(df)
    else:
        df = convert_diagnoses(df)

    # x_train, x_test = create_input_old(df)
    x_train, x_test = create_input(df)

    # print("--- %s seconds ---" % (time.time() - start_time))

    # Output to files
    out_directory = os.path.join(DATA, 'interim', 'retain')

    x_train.to_pickle(out_directory + '/data_train.pkl')
    x_test.sort_index().to_pickle(out_directory + '/data_test.pkl')
    y_train.sort_index().to_pickle(out_directory + '/target_train.pkl')
    y_test.sort_index().to_pickle(out_directory + '/target_test.pkl')


def count_diagnoses(num_patients=None, ccs=True, combine_diagnoses=False):
    start_time = time.time()
    df_tbi = load_mapping(FOLDER + 'patient_list')
    if num_patients is not None:
        df_tbi = df_tbi[:num_patients]
    df = load_dataset(FOLDER + 'dc_outpatient.feather')
    df = df[df['PatientID'].isin(df_tbi['PatientID'].unique())]
    df = df[df['PatientID'].isin(df[(df['TBIDays'] >= -365) & (df['TBIDays'] <= MIN_DAYS)]['PatientID'].unique())]
    df = df.reset_index(drop=True)
    df_tbi = df_tbi.reset_index(drop=True)

    df = df.sort_values(by=['PatientID', 'TBIDays'], ascending=[True, True])
    df_tbi = df_tbi.sort_values(by='PatientID', ascending=True)
    y_train, y_test = compute_outcome(df, df_tbi)
    if ccs:
        df = map_diagnoses(df)
    else:
        df = convert_diagnoses(df)
    print("after load %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    num_diagnoses = len(get_unique_diagnoses(df, display=False))

    df = df.rename(columns={'Diagnosis1': 'D_1', 'Diagnosis2': 'D_2', 'Diagnosis3': 'D_3'})
    df = pd.get_dummies(df, columns=['D_1', 'D_2', 'D_3'])
    print("finished dummies %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    diagnosis_columns = [col for col in df.columns if col.startswith('D_')]

    if combine_diagnoses:
        all_diagnoses = ['D_' + str(i + 1) + '_' + str(j) for i in range(3) for j in range(num_diagnoses)]

        missing_diagnoses = list(set(all_diagnoses) - set(diagnosis_columns))
        print('num missing', len(missing_diagnoses))

        # df = pd.concat([df, pd.DataFrame(columns=missing_diagnoses)])
        # df[missing_diagnoses] = 0
        # for d in missing_diagnoses:
        #     df[d] = 0

        # columns_drop = []
        # diagnosis_columns = []
        # for i in range(0, 279):
        #     name = 'Diagnosis_' + str(i)
        #     diagnosis_columns.append('Diagnosis_' + str(i))
        #     df[name] = 0
        #     for d in ['Diagnosis1', 'Diagnosis2', 'Diagnosis3']:
        #         if d + '_' + str(i) in df.columns:
        #             df[name] += df[d + '_' + str(i)]
        #             columns_drop.append(d + '_' + str(i))

        print("added missing diagnoses %s seconds ---" % (time.time() - start_time))
        start_time = time.time()

    x = df.groupby('PatientID').sum()[diagnosis_columns].values

    print("groupby values %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    print(x.shape)

    x_train, x_test = train_test_split(x, train_size=0.7, random_state=12345)

    return x_train, y_train, x_test, y_test


if __name__ == '__main__':
    create_data(num_patients=5000)
    # count_diagnoses(num_patients=5000)
