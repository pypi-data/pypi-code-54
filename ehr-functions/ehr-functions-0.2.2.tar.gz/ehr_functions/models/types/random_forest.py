from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor as RFR


class RandomForest(SKLearnModel):
    def __init__(self, **kwargs):
        super().__init__(RandomForestClassifier, kwargs)


class RandomForestRegressor(SKLearnModel):
    def __init__(self, **kwargs):
        super().__init__(RFR, kwargs)
