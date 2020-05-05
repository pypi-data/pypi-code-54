from ehr_functions.models.types._gridsearch import GridSearchModel
from sklearn.linear_model import LogisticRegression as LogR
import numpy as np


class LogisticRegressionGrid(GridSearchModel):
    def __init__(self, **kwargs):
        kwargs['solver'] = 'liblinear'
        super().__init__(LogR, {
            'C': np.logspace(-4, 4, 20),
            'penalty': ['l1', 'l2'],
        }, **kwargs)
