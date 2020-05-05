"""Implementation of RETAIN Keras from Edward Choi"""
import argparse
import os

import pandas as pd
from livelossplot.keras import PlotLossesCallback

from ehr_functions.models.retain_experiment.retain.callbacks import create_callbacks
from ehr_functions.models.retain_experiment.retain.model import model_create
from ehr_functions.models.retain_experiment.retain.sequence_builder import SequenceBuilder
from ehr_functions.paths import DATA


def read_nicoe_data():
    x_train_df = pd.read_pickle('data/data_train.pkl')
    x_test_df = pd.read_pickle('data/data_test.pkl')
    y_train = pd.read_pickle('data/target_train.pkl')
    y_test = pd.read_pickle('data/target_test.pkl')
    # x_train, y_train, x_test, y_test = create_all()

    y_train = y_train['target'].values
    y_test = y_test['target'].values

    x_train = [x_train_df['codes'].values]
    x_test = [x_test_df['codes'].values]

    if ARGS.numeric_size:
        x_train.append(x_train_df['numerics'].values)
        x_test.append(x_test_df['numerics'].values)
    if ARGS.use_time:
        x_train.append(x_train_df['to_event'].values)
        x_test.append(x_test_df['to_event'].values)

    return x_train, y_train, x_test, y_test


def read_data(ARGS):
    """Read the data from provided paths and assign it into lists"""
    folder = os.path.join(DATA, 'interim', 'retain')

    data_train_df = pd.read_pickle(os.path.join(folder, ARGS.path_data_train))
    data_test_df = pd.read_pickle(os.path.join(folder, ARGS.path_data_test))
    y_train = pd.read_pickle(os.path.join(folder, ARGS.path_target_train))['target'].values
    y_test = pd.read_pickle(os.path.join(folder, ARGS.path_target_test))['target'].values
    data_output_train = [data_train_df['codes'].values]
    data_output_test = [data_test_df['codes'].values]

    if ARGS.numeric_size:
        data_output_train.append(data_train_df['numerics'].values)
        data_output_test.append(data_test_df['numerics'].values)
    if ARGS.use_time:
        data_output_train.append(data_train_df['to_event'].values)
        data_output_test.append(data_test_df['to_event'].values)

    return data_output_train, y_train, data_output_test, y_test


def train_model(model, data_train, y_train, data_test, y_test, ARGS):
    """Train the Model with appropriate callbacks and generator"""
    checkpoint, log = create_callbacks(model, (data_test, y_test), ARGS)

    train_generator = SequenceBuilder(data=data_train, target=y_train,
                                      batch_size=ARGS.batch_size, ARGS=ARGS)

    val_generator = SequenceBuilder(data=data_test, target=y_test,
                                      batch_size=ARGS.batch_size, ARGS=ARGS)
    model.fit_generator(generator=train_generator, validation_data=val_generator, epochs=ARGS.epochs,
                        max_queue_size=15, use_multiprocessing=True,
                        callbacks=[checkpoint, log, PlotLossesCallback()], verbose=1, workers=3, initial_epoch=0)


def main(ARGS):
    """Main function"""
    print('Reading Data')
    data_train, y_train, data_test, y_test = read_data(ARGS)
    # data_train, y_train, data_test, y_test = read_nicoe_data()

    print('Creating Model')
    model = model_create(ARGS)

    print('Training Model')
    train_model(model=model, data_train=data_train, y_train=y_train,
                data_test=data_test, y_test=y_test, ARGS=ARGS)


def parse_arguments(custom_args=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    """Read user arguments"""
    parser.add_argument('--num_codes', type=int, required=True,
                        help='Number of medical codes')
    parser.add_argument('--numeric_size', type=int, default=0,
                        help='Size of numeric inputs, 0 if none')
    parser.add_argument('--use_time', action='store_true',
                        help='If argument is present the time input will be used')
    parser.add_argument('--emb_size', type=int, default=200,
                        help='Size of the embedding layer')
    parser.add_argument('--epochs', type=int, default=1,
                        help='Number of epochs')
    parser.add_argument('--n_steps', type=int, default=300,
                        help='Maximum number of visits after which the data is truncated')
    parser.add_argument('--recurrent_size', type=int, default=200,
                        help='Size of the recurrent layers')
    parser.add_argument('--path_data_train', type=str, default='data_train.pkl',
                        help='Path to train data')
    parser.add_argument('--path_data_test', type=str, default='data_test.pkl',
                        help='Path to test data')
    parser.add_argument('--path_target_train', type=str, default='target_train.pkl',
                        help='Path to train target')
    parser.add_argument('--path_target_test', type=str, default='target_test.pkl',
                        help='Path to test target')
    parser.add_argument('--batch_size', type=int, default=32,
                        help='Batch Size')
    parser.add_argument('--dropout_input', type=float, default=0.0,
                        help='Dropout rate for embedding')
    parser.add_argument('--dropout_context', type=float, default=0.0,
                        help='Dropout rate for context vector')
    parser.add_argument('--l2', type=float, default=0.0,
                        help='L2 regularitzation value')
    parser.add_argument('--directory', type=str, default=os.path.join(DATA, 'interim', 'retain'),
                        help='Directory to save the model and the log file to')
    parser.add_argument('--allow_negative', action='store_true',
                        help='If argument is present the negative weights for embeddings/attentions\
                         will be allowed (original RETAIN implementaiton)')

    # my_arguments = '--num_codes 20000'
    # my_arguments = '--num_codes 136'
    # my_arguments = '--num_codes 9602'

    if custom_args is not None:
        args = parser.parse_args(custom_args.split())
    else:
        args = parser.parse_args()

    return args


def run_model(num_codes, epochs=None, use_time=None, numeric_size=None, emb_size=None, recurrent_size=None,
              allow_negative=None, dropout_input=None, dropout_context=None, batch_size=None):
    argument_string = '--num_codes ' + str(num_codes)
    if epochs is not None:
        argument_string += ' --epochs ' + str(epochs)

    if use_time is not None:
        argument_string += ' --use_time'

    if numeric_size is not None:
        argument_string += ' --numeric_size ' + str(numeric_size)

    if emb_size is not None:
        argument_string += ' --emb_size ' + str(emb_size)

    if recurrent_size is not None:
        argument_string += ' --recurrent_size ' + str(recurrent_size)

    if allow_negative is not None:
        argument_string += ' --allow_negative'

    if dropout_input is not None:
        argument_string += ' --dropout_input ' + str(dropout_input)

    if dropout_context is not None:
        argument_string += ' --dropout_context ' + str(dropout_context)

    if batch_size is not None:
        argument_string += ' --batch_size ' + str(batch_size)

    ARGS = parse_arguments(argument_string)
    main(ARGS)


if __name__ == '__main__':
    ARGS = parse_arguments()
    main(ARGS)
