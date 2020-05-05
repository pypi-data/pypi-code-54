from ehr_functions.models.types import NeuralNetwork
from ehr_functions.paths import DATA
import tensorflowjs as tfjs
import keras.backend as K
from keras.models import load_model
import datetime
import json
import os


def save_model(model, folder, model_name):
    folder = os.path.join(DATA, 'processed', folder, model_name)
    if isinstance(model, NeuralNetwork):
        model = model.model
    tfjs.converters.save_keras_model(model, folder)

    with open(os.path.join(folder, 'time.txt'), 'w') as w:
        w.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def complicated_save(model, folder, model_name):
    # Save using the keras save function
    path = os.path.join(DATA, 'processed', folder, 'model.h5')
    model.model.save(path)

    # Clear the tensorflow path
    K.clear_session()

    # Load the model back and delete the file
    model = load_model(path)
    os.remove(path)

    # Now officially save using
    save_model(model, folder, model_name)


def export_patients(df, df_tbi, features, features_config, folder):
    folder = os.path.join(DATA, 'processed', folder)

    df.to_csv(os.path.join(folder, 'encounters.csv'), index=False)
    df_tbi.to_csv(os.path.join(folder, 'tbi.csv'), index=False)
    features.to_csv(os.path.join(folder, 'features.csv'), index=False)

    with open(os.path.join(folder, 'features_config.json'), 'w') as w:
        json.dump(features_config, w)
