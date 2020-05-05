from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import pandas as pd


def select_k_best(features, outcome, k=5, score_func=chi2):
    feature_columns = [col for col in features.columns if col != 'PatientID']
    outcome_columns = [col for col in outcome.columns if col != 'PatientID']

    df = pd.merge(features, outcome, on='PatientID', how='outer')

    df = df.fillna(0)

    x = df[feature_columns].values
    y = df[outcome_columns].values

    selector = SelectKBest(score_func=score_func, k=k)

    x = selector.fit_transform(x, y)

    return pd.concat([df[['PatientID']].reset_index(drop=True), pd.DataFrame(x)], axis=1)
