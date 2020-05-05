from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.linear_model import ElasticNet as EN
import numpy as np


class ElasticNet(SKLearnModel):
    def __init__(self, round_output=False, **kwargs):
        super().__init__(EN, kwargs)
        self.round_output = round_output

    def predict(self, x):
        output = super().predict(x)
        if self.round_output:
            output = np.round(output)

        return output
