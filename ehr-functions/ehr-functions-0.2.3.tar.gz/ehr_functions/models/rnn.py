from keras import Input, Model
from keras.layers import Dense, Embedding, Concatenate, LSTM
from keras.preprocessing.sequence import pad_sequences
import numpy as np


def predict(diagnosis_1, diagnosis_2, diagnosis_3, y, demographics, num_diagnoses=50):
    NUM_PATIENTS = diagnosis_1.shape[0]
    NUM_TIMESTEPS = diagnosis_1.shape[1]

    # demographics = np.zeros((NUM_PATIENTS, 50))
    # diagnosis_1 = np.zeros((NUM_PATIENTS, NUM_TIMESTEPS))
    # diagnosis_2 = np.zeros((NUM_PATIENTS, NUM_TIMESTEPS))
    # diagnosis_3 = np.zeros((NUM_PATIENTS, NUM_TIMESTEPS))
    # y = np.ones((NUM_PATIENTS, 1))
    print('y.shape', y.shape)
    print('demographics.shape', demographics.shape)
    print('diagnosis_1.shape', diagnosis_1.shape)
    print('diagnosis_2.shape', diagnosis_2.shape)

    input_demographics = Input(shape=(demographics.shape[1],))
    input_diagnosis_1 = Input(shape=(NUM_TIMESTEPS,))
    input_diagnosis_2 = Input(shape=(NUM_TIMESTEPS,))
    input_diagnosis_3 = Input(shape=(NUM_TIMESTEPS,))
    e_diagnoses = Embedding(num_diagnoses, 100)

    input_all = Concatenate(axis=1)([
        e_diagnoses(input_diagnosis_1),
        e_diagnoses(input_diagnosis_2),
        e_diagnoses(input_diagnosis_3)
    ])

    # Hidden
    h = LSTM(50, activation='tanh')(input_all)

    h_dem = Dense(50, activation='relu')(input_demographics)

    h_all = Concatenate(axis=1)([h, h_dem])

    h_final = Dense(50, activation='relu')(h_all)

    # Output
    o = Dense(1, activation='softmax')(h_final)

    model = Model(inputs=[input_demographics, input_diagnosis_1, input_diagnosis_2, input_diagnosis_3], outputs=o)
    model.compile(optimizer='rmsprop', loss='binary_crossentropy')
    model.fit([demographics, diagnosis_1, diagnosis_2, diagnosis_3], y, epochs=4, verbose=2, batch_size=100)


if __name__ == '__main__':
    from ehr_functions.data.load_dataset import load_dataset

    FOLDER = 'interim/all/'
    FILE = 'dc_outpatient_encounters.feather'
    # FILE = 'pc_inpatient_encounters.feather'

    df = load_dataset(FOLDER + FILE, num_patients=10000)

    from ehr_functions.features.code_descriptions import get_tbi

    tbi_codes = get_tbi()

    print(tbi_codes[:5])

    from ehr_functions.features.filter_dataset import get_occurrence, calculate_days

    df_tbi = get_occurrence(df, tbi_codes, nth=0)
    df, df_tbi = calculate_days(df, df_tbi, 'TBI')

    from ehr_functions.features.filter_dataset import get_patients_had_encounters, limit_df

    patient_ids = get_patients_had_encounters(df)
    df = limit_df(df, patient_ids)

    df['PatientID'].nunique()

    from ehr_functions.features.code_descriptions import get_depression

    depression_codes = get_depression()

    from ehr_functions.features.filter_dataset import tag_had_code

    df = tag_had_code(df, df['TBIDays'] > 0, 'GotDepression', depression_codes, nth=3)

    from ehr_functions.features.build_features import build_demographics
    df = df[(df['TBIDays'] > -365) & (df['TBIDays'] <= 0)]

    demographics = build_demographics(df)
    demographics = demographics.drop(columns='PatientID')
    demographics = demographics.values

    y = df[['PatientID', 'GotDepression']]
    y = y.drop_duplicates()
    y = np.asarray(y['GotDepression'].tolist())

    diagnoses = df['Diagnosis1'].unique().tolist()
    diagnoses += df['Diagnosis2'].unique().tolist()
    diagnoses += df['Diagnosis3'].unique().tolist()

    diagnoses_dict = {k: v for v, k in enumerate(diagnoses)}
    df['Diagnosis1'] = df['Diagnosis1'].map(diagnoses_dict)
    df['Diagnosis2'] = df['Diagnosis2'].map(diagnoses_dict)
    df['Diagnosis3'] = df['Diagnosis3'].map(diagnoses_dict)

    df = df[['PatientID', 'EncounterDate', 'Diagnosis1', 'Diagnosis2', 'Diagnosis3']]
    patients = df.groupby(['PatientID'])

    diagnosis_1 = patients['Diagnosis1'].apply(lambda x: x.values.tolist()).values
    diagnosis_2 = patients['Diagnosis2'].apply(lambda x: x.values.tolist()).values
    diagnosis_3 = patients['Diagnosis3'].apply(lambda x: x.values.tolist()).values
    diagnosis_1 = diagnosis_1.tolist()
    diagnosis_2 = diagnosis_2.tolist()
    diagnosis_3 = diagnosis_3.tolist()

    lengths = [len(patient) for patient in diagnosis_1]
    lengths += [len(patient) for patient in diagnosis_2]
    lengths += [len(patient) for patient in diagnosis_3]

    max_len = max(lengths)
    print('max_length', max_len)

    diagnosis_1 = pad_sequences(diagnosis_1, maxlen=max_len)
    diagnosis_2 = pad_sequences(diagnosis_2, maxlen=max_len)
    diagnosis_3 = pad_sequences(diagnosis_3, maxlen=max_len)

    predict(diagnosis_1, diagnosis_2, diagnosis_3, y, demographics, num_diagnoses=len(diagnoses))
