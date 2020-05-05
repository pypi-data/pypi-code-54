from ehr_functions.data.load_dataset import load_dataset
from keras import Input, Model
from keras.layers import Dense, Embedding, Concatenate
import pandas as pd


def __model(demographics, diagnoses, meds, y):
    hidden_size = 64
    output_size = 1

    input_demographics = Embedding(input_length=demographics.shape[1])
    input_diagnoses = Embedding(input_length=diagnoses.shape[1])
    # input_meds = Embedding(input_length=meds.shape[1])

    input_all = Concatenate([input_demographics, input_diagnoses])

    # Hidden
    h = Dense(hidden_size, activation='relu')(input_all)

    # Output
    o = Dense(output_size, activation='softmax')(h)

    model = Model(inputs=[input_demographics, input_diagnoses], outputs=o)
    model.compile(optimizer='adam', loss='mse')
    model.fit([demographics, diagnoses, meds], y, epochs=1, verbose=2)


if __name__ == '__main__':
    FOLDER = 'interim/all/'
    # FILE = 'dc_outpatient_encounters.feather'
    FILE = 'pc_inpatient_encounters.feather'

    df = load_dataset(FOLDER + FILE, num_patients=10000)
    print('finished loading dataset')

    from ehr_functions.data.load_dataset import load_meds

    df_meds = load_meds()
    print('finished loading meds')

    from ehr_functions.features.code_descriptions import get_tbi

    tbi_codes = get_tbi()

    print(tbi_codes[:5])

    from ehr_functions.features.filter_dataset import get_occurrence, calculate_days

    df_tbi = get_occurrence(df, tbi_codes, nth=0)
    df, df_tbi = calculate_days(df, df_tbi, 'TBI')

    from ehr_functions.features.filter_dataset import get_patients_had_encounters, limit_df

    patient_ids = get_patients_had_encounters(df)
    df = limit_df(df, patient_ids)
    df_meds = limit_df(df_meds, patient_ids)

    df['PatientID'].nunique()

    from ehr_functions.features.code_descriptions import get_depression

    depression_codes = get_depression()

    from ehr_functions.features.filter_dataset import tag_had_code

    df = tag_had_code(df, df['TBIDays'] > 0, 'GotDepression', depression_codes, nth=3)

    from ehr_functions.features.build_features import build_demographics, build_encounter_info
    from ehr_functions.features.meds import get_med_features
    from ehr_functions.features.build_features import get_xy

    # Demographics

    features = build_demographics(df)

    df = df.drop(columns=['Diagnosis2', 'Diagnosis3'])

    from ehr_functions.features.build_features import simplify_codes, convert_category
    from ehr_functions.features.convert_codes import convert_codes_ccs_mapping

    df = convert_codes_ccs_mapping(df, ['Diagnosis1'])  # , 'Diagnosis2', 'Diagnosis3'])
    df, _ = convert_category(df, ['Diagnosis1'])  # , 'Diagnosis2', 'Diagnosis3'])

    # +
    features_encounters = build_encounter_info(df, groupings=[[0, 365]], prior=True)
    features = features.merge(features_encounters, on='PatientID', how='left')
