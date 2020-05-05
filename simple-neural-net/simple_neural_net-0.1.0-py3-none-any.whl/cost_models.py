import numpy as np

class CostModel:
    def cost(outputs, y):
        # outputs: (num_outputs, num_examples)
        # cost: Scalar
        raise NotImplementedError('Method must be implemented by child class')

    def d_cost_d_outputs(outputs, y):
        # outputs: (num_outputs, num_examples)
        # d_cost_d_outputs: (num_outputs, num_examples)
        raise NotImplementedError('Method must be implemented by child class')

class CrossEntropyBinaryClassificationCostModel(CostModel):
    def cost(
        self,
        outputs,
        y
    ):
        # outputs: (1, num_examples)
        # y: (1, num_examples)
        # cost: Scalar

        # outputs: For this cost function, outputs[0, i] is interpreted as the
        # probability that the ith example is of class 1 (as opposed to class 0)

        # y: For this cost function, y[0, i] is either 0
        # (first class) or 1 (second class)

        num_examples = y.shape[1]
        return np.squeeze(-(1/num_examples)*np.sum(
            np.add(
                np.multiply(
                    y,
                    np.log(outputs)
                ),
                np.multiply(
                    np.subtract(1.0, y),
                    np.log(np.subtract(1.0, outputs))
                )
            ),
            axis=1
        ))

    def d_cost_d_outputs(
        self,
        outputs,
        y
    ):
        # outputs: (num_outputs, num_examples)
        # y: (num_classes, num_examples)
        # d_cost_d_outputs: (num_outputs, num_examples)

        # outputs: For this cost function, outputs[0, i] is interpreted as the
        # probability that the ith example is of class 1 (as opposed to class 0)

        # y: For this cost function, y[0, i] is either 0
        # (first class) or 1 (second class)

        num_examples = y.shape[1]
        return -(1/num_examples)*np.divide(
            np.subtract(
                y,
                outputs
            ),
            np.multiply(
                outputs,
                np.subtract(1, outputs)
            )
        )
