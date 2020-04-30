# Copyright 2019 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sklearn.ensemble.gradient_boosting
import lale.docstrings
import lale.operators

class GradientBoostingClassifierImpl():

    def __init__(self, loss='deviance', learning_rate=0.1, n_estimators=100, subsample=1.0, criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_depth=3, min_impurity_decrease=0.0, min_impurity_split=None, init=None, random_state=None, max_features=None, verbose=0, max_leaf_nodes=None, warm_start=False, presort=None, validation_fraction=0.1, n_iter_no_change=None, tol=0.0001):
        self._hyperparams = {
            'loss': loss,
            'learning_rate': learning_rate,
            'n_estimators': n_estimators,
            'subsample': subsample,
            'criterion': criterion,
            'min_samples_split': min_samples_split,
            'min_samples_leaf': min_samples_leaf,
            'min_weight_fraction_leaf': min_weight_fraction_leaf,
            'max_depth': max_depth,
            'min_impurity_decrease': min_impurity_decrease,
            'min_impurity_split': min_impurity_split,
            'init': init,
            'random_state': random_state,
            'max_features': max_features,
            'verbose': verbose,
            'max_leaf_nodes': max_leaf_nodes,
            'warm_start': warm_start,
            'presort': presort,
            'validation_fraction': validation_fraction,
            'n_iter_no_change': n_iter_no_change,
            'tol': tol}
        self._wrapped_model = sklearn.ensemble.gradient_boosting.GradientBoostingClassifier(**self._hyperparams)

    def fit(self, X, y, **fit_params):
        if fit_params is None:
            self._wrapped_model.fit(X, y)
        else:
            self._wrapped_model.fit(X, y, **fit_params)
        return self

    def predict(self, X):
        return self._wrapped_model.predict(X)

    def predict_proba(self, X):
        return self._wrapped_model.predict_proba(X)

    def decision_function(self, X):
        return self._wrapped_model.decision_function(X)

_hyperparams_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Gradient Boosting for classification.',
    'allOf': [{
        'type': 'object',
        'required': ['init', 'presort'],
        'relevantToOptimizer': ['loss', 'learning_rate', 'n_estimators', 'subsample', 'min_samples_split', 'min_samples_leaf', 'max_depth', 'max_features', 'presort', 'n_iter_no_change', 'tol'],
        'additionalProperties': False,
        'properties': {
            'loss': {
                'enum': ['deviance', 'exponential'],
                'default': 'deviance',
                'description': "loss function to be optimized. 'deviance' refers to"},
            'learning_rate': {
                'type': 'number',
                'minimumForOptimizer': 0.01,
                'maximumForOptimizer': 1.0,
                'distribution': 'loguniform',
                'default': 0.1,
                'description': 'learning rate shrinks the contribution of each tree by `learning_rate`.'},
            'n_estimators': {
                'type': 'integer',
                'minimumForOptimizer': 10,
                'maximumForOptimizer': 100,
                'distribution': 'uniform',
                'default': 100,
                'description': 'The number of boosting stages to perform. Gradient boosting'},
            'subsample': {
                'type': 'number',
                'minimumForOptimizer': 0.01,
                'maximumForOptimizer': 1.0,
                'distribution': 'uniform',
                'default': 1.0,
                'description': 'The fraction of samples to be used for fitting the individual base'},
            'criterion': {
                'enum': ['friedman_mse', 'mse', 'mae'],
                'default': 'friedman_mse',
                'description': 'The function to measure the quality of a split. Supported criteria'},
            'min_samples_split': {
                'anyOf': [{
                    'type': 'integer',
                    'minimumForOptimizer': 2,
                    'maximumForOptimizer': 20,
                    'distribution': 'uniform'}, {
                    'type': 'number',
                    'minimumForOptimizer': 0.01,
                    'maximumForOptimizer': 0.5}],
                'default': 2,
                'description': 'The minimum number of samples required to split an internal node:'},
            'min_samples_leaf': {
                'anyOf': [{
                    'type': 'integer',
                    'minimumForOptimizer': 1,
                    'maximumForOptimizer': 20,
                    'distribution': 'uniform'}, {
                    'type': 'number',
                    'minimumForOptimizer': 0.01,
                    'maximumForOptimizer': 0.5}],
                'default': 1,
                'description': 'The minimum number of samples required to be at a leaf node.'},
            'min_weight_fraction_leaf': {
                'type': 'number',
                'default': 0.0,
                'description': 'The minimum weighted fraction of the sum total of weights (of all'},
            'max_depth': {
                'type': 'integer',
                'minimumForOptimizer': 3,
                'maximumForOptimizer': 5,
                'default': 3,
                'description': 'maximum depth of the individual regression estimators. The maximum'},
            'min_impurity_decrease': {
                'type': 'number',
                'default': 0.0,
                'description': 'A node will be split if this split induces a decrease of the impurity'},
            'min_impurity_split': {
                'anyOf': [{
                    'type': 'number'}, {
                    'enum': [None]}],
                'default': None,
                'description': 'Threshold for early stopping in tree growth. A node will split'},
            'init': {
                'anyOf': [{
                    'type': 'object'}, {
                    'enum': ['zero', None]}],
                'default': None,
                'description': 'An estimator object that is used to compute the initial'},
            'random_state': {
                'anyOf': [{
                    'type': 'integer'}, {
                    'type': 'object'}, {
                    'enum': [None]}],
                'default': None,
                'description': 'If int, random_state is the seed used by the random number generator;'},
            'max_features': {
                'anyOf': [{
                    'type': 'integer',
                    'forOptimizer': False}, {
                    'type': 'number',
                    'minimum': 0.0,
                    'exclusiveMinimum': True,
                    'minimumForOptimizer': 0.0,
                    'maximumForOptimizer': 1.0,
                    'distribution': 'uniform'}, {
                    'enum': ['auto', 'sqrt', 'log2', None]}],
                'default': None,
                'description': 'The number of features to consider when looking for the best split:'},
            'verbose': {
                'type': 'integer',
                'default': 0,
                'description': 'Enable verbose output. If 1 then it prints progress and performance'},
            'max_leaf_nodes': {
                'anyOf': [{
                    'type': 'integer'}, {
                    'enum': [None]}],
                'default': None,
                'description': 'Grow trees with ``max_leaf_nodes`` in best-first fashion.'},
            'warm_start': {
                'type': 'boolean',
                'default': False,
                'description': 'When set to ``True``, reuse the solution of the previous call to fit'},
            'presort': {
                'anyOf': [{
                    'type': 'boolean'}, {
                    'enum': ['auto']}],
                'default': 'auto',
                'description': 'Whether to presort the data to speed up the finding of best splits in'},
            'validation_fraction': {
                'type': 'number',
                'default': 0.1,
                'description': 'The proportion of training data to set aside as validation set for'},
            'n_iter_no_change': {
                'anyOf': [{
                    'type': 'integer',
                    'minimumForOptimizer': 5,
                    'maximumForOptimizer': 10}, {
                    'enum': [None]}],
                'default': None,
                'description': '``n_iter_no_change`` is used to decide if early stopping will be used'},
            'tol': {
                'type': 'number',
                'minimumForOptimizer': 1e-08,
                'maximumForOptimizer': 0.01,
                'distribution': 'loguniform',
                'default': 0.0001,
                'description': 'Tolerance for the early stopping. When the loss is not improving'},
        }}]}

_input_fit_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Fit the gradient boosting model.',
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
            'description': 'The input samples. Internally, it will be converted to'},
        'y': {
            'anyOf': [
                {'type': 'array', 'items': {'type': 'number'}},
                {'type': 'array', 'items': {'type': 'string'}}],
            'description': 'Target values (strings or integers in classification, real numbers'},
        'sample_weight': {
            'anyOf': [{
                'type': 'array',
                'items': {
                    'type': 'number'},
            }, {
                'enum': [None]}],
            'default': None,
            'description': 'Sample weights. If None, then samples are equally weighted. Splits'},
        'monitor': {
            'type': 'object', #callable, optional
            'description': 'The monitor is called after each iteration with the current'},
    },
}
_input_predict_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Predict class for X.',
    'type': 'object',
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'The input samples. Internally, it will be converted to'},
    },
}
_output_predict_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'The predicted values.',
    'anyOf': [
        {'type': 'array', 'items': {'type': 'number'}},
        {'type': 'array', 'items': {'type': 'string'}}]}

_input_predict_proba_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'Predict class probabilities for X.',
    'type': 'object',
    'properties': {
        'X': {
            'type': 'array',
            'items': {
                'type': 'array',
                'items': {
                    'type': 'number'},
            },
            'description': 'The input samples. Internally, it will be converted to'},
    },
}
_output_predict_proba_schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': 'The class probabilities of the input samples. The order of the',
    'type': 'array',
    'items': {
        'type': 'array',
        'items': {
            'type': 'number'},
    },
}

_input_decision_function_schema = {
  'type': 'object',
  'required': ['X'],
  'additionalProperties': False,
  'properties': {
    'X': {
      'description': 'Features; the outer array is over samples.',
      'type': 'array',
      'items': {'type': 'array', 'items': {'type': 'number'}}}}}

_output_decision_function_schema = {
    'description': 'Confidence scores for samples for each class in the model.',
    'anyOf': [
    {   'description': 'In the multi-way case, score per (sample, class) combination.',
        'type': 'array',
        'items': {'type': 'array', 'items': {'type': 'number'}}},
    {   'description': 'In the binary case, score for `self._classes[1]`.',
        'type': 'array',
        'items': {'type': 'number'}}]}

_combined_schemas = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'description': """`Gradient boosting classifier`_ random forest from scikit-learn.

.. _`Gradient boosting classifier`: https://scikit-learn.org/0.20/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn-ensemble-gradientboostingclassifier
""",
    'documentation_url': 'https://lale.readthedocs.io/en/latest/modules/lale.lib.sklearn.gradient_boosting_classifier.html',
    'type': 'object',
    'tags': {
        'pre': [],
        'op': ['estimator', 'classifier'],
        'post': []},
    'properties': {
        'hyperparams': _hyperparams_schema,
        'input_fit': _input_fit_schema,
        'input_predict': _input_predict_schema,
        'output_predict': _output_predict_schema,
        'input_predict_proba': _input_predict_proba_schema,
        'output_predict_proba': _output_predict_proba_schema,
        'input_decision_function': _input_decision_function_schema,
        'output_decision_function': _output_decision_function_schema,
}}

lale.docstrings.set_docstrings(GradientBoostingClassifierImpl, _combined_schemas)

GradientBoostingClassifier = lale.operators.make_operator(GradientBoostingClassifierImpl, _combined_schemas)
