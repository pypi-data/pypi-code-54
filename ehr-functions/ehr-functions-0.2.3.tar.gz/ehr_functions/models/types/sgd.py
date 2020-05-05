from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.linear_model import SGDClassifier
import numpy as np


class SGD(SKLearnModel):
    def __init__(self, round_output=False, **kwargs):
        super().__init__(SGDClassifier, kwargs)
        self.round_output = round_output

    def predict(self, x):
        output = super().predict(x)
        if self.round_output:
            output = np.round(output)

        return output
