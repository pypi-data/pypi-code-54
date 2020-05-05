from ehr_functions.data.load_dataset import load_dataset
from keras import Input, Model
from keras.layers import Dense
import pandas as pd


def __autoencoder(data):
    input_size = data.shape[1]
    hidden_size = 64
    output_size = data.shape[1]

    x = Input(shape=(input_size,))

    # Encoder
    h = Dense(hidden_size, activation='relu')(x)

    # Decoder
    r = Dense(output_size, activation='relu')(h)

    autoencoder = Model(inputs=x, outputs=r)
    autoencoder.compile(optimizer='adam', loss='mse')
    autoencoder.fit(data, data, epochs=20, verbose=2)

    hidden_model = Model(inputs=x, outputs=h)
    return hidden_model.predict(data)


def reduce_features(df, columns):
    # Count number of diagnoses
    diagnoses = set()
    for col in columns:
        diagnoses = diagnoses.union(set(df[col].unique().tolist()))

    diagnoses = list(diagnoses)
    diagnoses.remove('')

    # Make big df of all patient id's and diagnoses
    patient_ids = []
    diagnoses = []
    for col in columns:
        patient_ids += df['PatientID'].tolist()
        diagnoses += df[col].tolist()
    big_df = pd.DataFrame({'PatientID': patient_ids, 'Diagnosis': diagnoses})
    diagnosis_counts = big_df.groupby('PatientID')['Diagnosis'].value_counts().unstack(fill_value=0)
    values = diagnosis_counts.values[:, 1:]

    result = __autoencoder(values)
    result = pd.DataFrame(result, columns=['AutoEncoder' + '_' + str(i) for i in range(64)])
    result['PatientID'] = df['PatientID']

    return result


if __name__ == '__main__':
    FOLDER = 'interim/all/'
    # FILE = 'dc_outpatient_encounters.feather'
    FILE = 'pc_inpatient_encounters.feather'

    df = load_dataset(FOLDER + FILE, num_patients=10000)
    print('finished loading dataset')

    df = df[['PatientID', 'Diagnosis1', 'Diagnosis2', 'Diagnosis3']]

    df = reduce_features(df, columns=['Diagnosis1', 'Diagnosis2', 'Diagnosis3'])
    print(df.shape)
    # print(df.columns.tolist())
