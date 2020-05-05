from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.ensemble import AdaBoostClassifier


class AdaBoost(SKLearnModel):
    def __init__(self, **kwargs):
        super().__init__(AdaBoostClassifier, kwargs)
