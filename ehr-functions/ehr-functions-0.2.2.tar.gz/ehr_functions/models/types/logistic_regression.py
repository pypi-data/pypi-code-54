from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.linear_model import LogisticRegression as LogR


class LogisticRegression(SKLearnModel):
    def __init__(self, **kwargs):
        super().__init__(LogR, kwargs)
