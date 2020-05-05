from ehr_functions.models.types._gridsearch import GridSearchModel
from sklearn.svm import SVC
import numpy as np


class SVMGrid(GridSearchModel):
    def __init__(self, **kwargs):
        super().__init__(SVC, [
            {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
            {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
        ], **kwargs)
