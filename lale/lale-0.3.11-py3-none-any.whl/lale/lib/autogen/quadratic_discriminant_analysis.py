
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as Op
import lale.helpers
import lale.operators
import lale.docstrings
from numpy import nan, inf

class QuadraticDiscriminantAnalysisImpl():

    def __init__(self, priors=None, reg_param=0.0, store_covariance=False, tol=0.0001, store_covariances=None):
        self._hyperparams = {
            'priors': priors,
            'reg_param': reg_param,
            'store_covariance': store_covariance,
            'tol': tol,
            'store_covariances': store_covariances}
        self._wrapped_model = Op(**self._hyperparams)

    def fit(self, X, y=None):
        if (y is not None):
            self._wrapped_model.fit(X, y)
        else:
            self._wrapped_model.fit(X)
        return self

    def predict(self, X):
        return self._wrapped_model.predict(X)

    def predict_proba(self, X):
        return self._wrapped_model.predict_proba(X)

    def decision_function(self, X):
        return self._wrapped_model.decision_function(X)
_hyperparams_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'inherited docstring for QuadraticDiscriminantAnalysis    Quadratic Discriminant Analysis',
    'allOf': [{
        'type': 'object',
        'required': ['priors', 'reg_param', 'store_covariance', 'tol', 'store_covariances'],
        'relevantToOptimizer': ['tol'],
        'additionalProperties': False,
        'properties': {
            'priors': {
                'XXX TODO XXX': 'array, optional, shape = [n_classes]',
                'description': 'Priors on classes',
                'enum': [None],
                'default': None},
            'reg_param': {
                'type': 'number',
                'default': 0.0,
                'description': 'Regularizes the covariance estimate as ``(1-reg_param)*Sigma + reg_param*np.eye(n_features)``'},
            'store_covariance': {
                'type': 'boolean',
                'default': False,
                'description': 'If True the covariance matrices are computed and stored in the `self.covariance_` attribute'},
            'tol': {
                'type': 'number',
                'minimumForOptimizer': 1e-08,
                'maximumForOptimizer': 0.01,
                'distribution': 'loguniform',
                'default': 0.0001,
                'description': 'Threshold used for rank estimation'},
            'store_covariances': {
                'anyOf': [{
                    'type': 'boolean'}, {
                    'enum': [None]}],
                'default': None,
                'description': 'Deprecated, use `store_covariance`.'},
        }}],
}
_input_fit_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Fit the model according to the given training data and parameters.',
    'type': 'object',
    'required': ['X', 'y'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'Training vector, where n_samples is the number of samples and n_features is the number of features.'},
        'y': {
            'type': 'array',
            'items': {
                'type': 'number'},
            'description': 'Target values (integers)'},
    },
}
_input_predict_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Perform classification on an array of test vectors X.',
    'type': 'object',
    'required': ['X'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            }},
    },
}
_output_predict_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Perform classification on an array of test vectors X.',
    'type': 'array',
    'items': {
        'type': 'number'},
}
_input_predict_proba_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Return posterior probabilities of classification.',
    'type': 'object',
    'required': ['X'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'Array of samples/test vectors.'},
    },
}
_output_predict_proba_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Posterior probabilities of classification per class.',
    'type': 'array',
    'items': {
        'type': 'array',
        'items': {
            'type': 'number'},
    },
}
_input_decision_function_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Apply decision function to an array of samples.',
    'type': 'object',
    'required': ['X'],
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'Array of samples (test vectors).'},
    },
}
_output_decision_function_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Decision function values related to each class, per sample',
    'anyOf': [{
        'type': 'array',
        'items': {
            'type': 'array',
            'items': {
                'type': 'number'},
        }}, {
        'type': 'array',
        'items': {
            'type': 'number'},
    }],
}
_combined_schemas = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Combined schema for expected data and hyperparameters.',
    'documentation_url': 'https://scikit-learn.org/0.20/modules/generated/sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis#sklearn-discriminant_analysis-quadraticdiscriminantanalysis',
    'type': 'object',
    'tags': {
        'pre': [],
        'op': ['estimator'],
        'post': []},
    'properties': {
        'hyperparams': _hyperparams_schema,
        'input_fit': _input_fit_schema,
        'input_predict': _input_predict_schema,
        'output_predict': _output_predict_schema,
        'input_predict_proba': _input_predict_proba_schema,
        'output_predict_proba': _output_predict_proba_schema,
        'input_decision_function': _input_decision_function_schema,
        'output_decision_function': _output_decision_function_schema},
}
lale.docstrings.set_docstrings(QuadraticDiscriminantAnalysisImpl, _combined_schemas)
QuadraticDiscriminantAnalysis = lale.operators.make_operator(QuadraticDiscriminantAnalysisImpl, _combined_schemas)

