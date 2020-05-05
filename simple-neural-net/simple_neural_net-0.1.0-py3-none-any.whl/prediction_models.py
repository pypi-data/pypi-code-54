import numpy as np

class PredictionModel:
    def predictions(
        self,
        outputs
    ):
        # outputs: (num_outputs, num_examples)
        # predictions: (?, num_examples)
        raise NotImplementedError('Method must be implemented by child class')

class BinaryClassificationPredictionModel(PredictionModel):
    def predictions(
        self,
        outputs
    ):
        # outputs: (1, num_examples)
        # predictions: (1, num_examples)
        y_hat = np.around(outputs).astype('int')
        return y_hat
