from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score, roc_auc_score

from ehr_functions.models.train_model import __fix_empty_array_shape
from ehr_functions.visualization.visualize import __has_continuous, __plot_roc_curve
import pandas as pd
import numpy as np
import copy


def show_results_prediction(test_true, test_pred):
    if np.unique(test_true).shape[0] <= 2:
        test_true = test_true.flatten()
        test_pred = test_pred.flatten()
        test_auc = roc_auc_score(test_true, test_pred, average='micro')

        __plot_roc_curve(test_true, test_pred)

        if not __has_continuous(test_true):
            test_pred = np.round(test_pred)

        test_acc = accuracy_score(test_true, test_pred) * 100
        print('Test Accuracy: ' + str(test_acc))
        print('Test AUC: ' + str(test_auc))
        print('')
        print('Test')
        print(classification_report(test_true, test_pred))
    else:
        test_mse = mean_squared_error(test_true, test_pred)
        test_r2 = r2_score(test_true, test_pred)
        print('Test Mean Squared Error: ' + str(test_mse))
        print('Test R^2: ' + str(test_r2))
    print('')


def __predict_test_data_model(model, df, features, outcomes):
    model = copy.deepcopy(model)

    df = df[df['Type'] == 'test']
    x_test, y_test = df[features].values, df[outcomes].values

    if len(outcomes) == 1:
        y_test = np.squeeze(y_test, axis=1)

    test_pred = model.predict(x_test)

    if len(test_pred.shape) > 1 and test_pred.shape[1] > 1:
        for i, col in enumerate(outcomes):
            print(col)
            show_results_prediction(y_test[:, i], test_pred[:, i])

        print('Overall')
        show_results_prediction(y_test, test_pred)
    else:
        print(outcomes)
        show_results_prediction(y_test, test_pred)

    return model, (y_test, test_pred)


def predict_test_data_model(model, features, outcome, lookup, outcome_columns=None, separate_models=False,
                            return_results=False):
    feature_columns = [col for col in features.columns if col != 'PatientID']
    if outcome_columns is None:
        outcome_columns = [col for col in outcome.columns if col != 'PatientID']
    df = pd.merge(features, outcome, on='PatientID', how='outer')
    df = df.fillna(0)

    df = pd.merge(df, lookup[['PatientID', 'Type']], on='PatientID', how='outer')

    if separate_models:
        y_true, y_pred = np.asarray([]), np.asarray([])
        for model, col in zip(model, outcome_columns):
            _, result = __predict_test_data_model(model, df, feature_columns, col)

            y_true = __fix_empty_array_shape(y_true, result[0])
            y_pred = __fix_empty_array_shape(y_pred, result[1])

            y_true = np.concatenate((y_true, result[0]))
            y_pred = np.concatenate((y_pred, result[1]))

        print('Overall')
        show_results_prediction(y_true, y_pred)
    else:
        model, results = __predict_test_data_model(model, df, feature_columns, outcome_columns)

    if return_results:
        return model, results
    return model
