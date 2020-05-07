
from sklearn.base import BaseEstimator, RegressorMixin
class ApproximationBase(BaseEstimator, RegressorMixin):
    def __init__(self, X=None, Y=None, fname=None, initDict=None, xmin=-1, xmax=1):
        if initDict is not None:
            self.mkFromDict(initDict)
        elif fname is not None:
            self.mkFromJSON(fname)
        elif X is not None and Y is not None:
            # self._m=order[0]
            # self._n=order[1]
            self._scaler = apprentice.Scaler(np.array(X, dtype=np.float64), a=xmin, b=xmax)
            self._X   = self._scaler.scaledPoints
            self._dim = self._X[0].shape[0]
            self._Y   = np.array(Y, dtype=np.float64)
            self._trainingsize=len(X)
            # self.fit(strategy=strategy)
        else:
            raise Exception("Constructor not called correctly, use either fname, initDict or X and Y")
