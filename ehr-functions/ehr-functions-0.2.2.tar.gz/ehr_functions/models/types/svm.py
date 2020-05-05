from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.svm import SVC


class SVM(SKLearnModel):
    def __init__(self, **kwargs):
        super().__init__(SVC, kwargs)
