from ehr_functions.models.types._sklearn import SKLearnModel
from sklearn.model_selection import GridSearchCV


class GridSearchModel(SKLearnModel):
    def __init__(self, model, param_grid, **kwargs):
        super().__init__(model, kwargs)  # This is here just to run it, bu then overwriting self.model
        self.model = GridSearchCV(model(**kwargs), param_grid, cv=5)

    def train(self, x, y):
        x, y = self._process_train_data(x, y)
        grid_result = self.model.fit(x, y)
        print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
