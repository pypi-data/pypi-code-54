from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.linear_model import LinearRegression as LinR


class LinearRegression(SKLearnModel):
    def __init__(self, **kwargs):
        super().__init__(LinR, kwargs)
