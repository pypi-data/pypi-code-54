from ..column_types import AnyTypePredictor, ItalianVATType, ItalianFiscalCodeType
from sklearn.preprocessing import LabelEncoder
from ..features import AnyFeature
import pandas as pd
import numpy as np


class DataframeEmbedding:

    def __init__(self):
        self._predictor = AnyTypePredictor()
        self._feature = AnyFeature()
        self._encoder = LabelEncoder().fit(self._predictor.supported_types)
        self._ivas = ItalianVATType()
        self._fiscal_codes = ItalianFiscalCodeType()

    def transform(self, df: pd.DataFrame, y: np.ndarray = None) -> np.ndarray:
        """Encode given dataframe into a vector space."""
        fiscal_codes = [None]*df.shape[0]
        ivas = [None]*df.shape[0]
        for column in df.columns:
            predictions = self._ivas.validate(df[column])
            if any(predictions):
                ivas = [
                    value if prediction else None
                    for value, prediction in zip(df[column].values, predictions)
                ]
                break

        for column in df.columns:
            predictions = self._fiscal_codes.validate(df[column])
            if any(predictions):
                fiscal_codes = [
                    value if prediction else None
                    for value, prediction in zip(df[column].values, predictions)
                ]

        column_x = []
        means = []

        for column in df.columns:
            predictions = pd.DataFrame({
                **self._predictor.predict(
                    df[column],
                    fiscal_codes=fiscal_codes,
                    ivas=ivas
                ),
                **self._feature.scores(df[column])
            })

            column_x.append(predictions.values)
            means.append(np.tile(predictions.values.mean(axis=0), (predictions.shape[0], 1)))

        column_x = np.vstack(column_x)
        means = np.vstack(means)
        global_means = np.tile(means.mean(axis=0), (column_x.shape[0], 1))

        X = np.hstack([
            column_x,
            means,
            global_means
        ])

        if y is not None:
            return X, self._encoder.transform(y.T.values.ravel())
        return X

    def reverse_label_embedding(self, encoded_labels: np.ndarray, df: pd.DataFrame) -> np.ndarray:
        decoded_labels = self._encoder.inverse_transform(encoded_labels)

        decoded_labels = decoded_labels.reshape((df.shape[1], df.shape[0]))

        return pd.DataFrame(
            decoded_labels.T,
            columns=df.columns,
            index=df.index
        )
