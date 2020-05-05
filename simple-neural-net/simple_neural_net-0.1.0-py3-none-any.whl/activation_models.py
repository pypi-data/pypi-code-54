import numpy as np

class ActivationModel:
    def activation(
        self,
        Z
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        raise NotImplementedError('Method must be implemented by child class')

    def d_activation_d_Z(
        self,
        Z,
        outputs
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        # d_activation_d_Z: (num_outputs, num_examples)
        raise NotImplementedError('Method must be implemented by child class')

class SigmoidActivationModel(ActivationModel):
    def activation(
        self,
        Z
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        return np.reciprocal(np.add(1.0, np.exp(-Z))) # (num_outputs, num_examples)

    def d_activation_d_Z(
        self,
        Z,
        outputs
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        # d_activation_d_Z: (num_outputs, num_examples)
        return np.multiply(outputs, np.subtract(1, outputs)) # (num_outputs, num_examples)

class TanhActivationModel(ActivationModel):
    def activation(
        self,
        Z
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        return np.tanh(Z) # (num_outputs, num_examples)

    def d_activation_d_Z(
        self,
        Z,
        outputs
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        # d_activation_d_Z: (num_outputs, num_examples)
        return np.subtract(1, np.square(outputs)) # (num_outputs, num_examples)

class ReLUActivationModel(ActivationModel):
    def activation(
        self,
        Z
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        return np.multiply(Z, Z > 0.0) # (num_outputs, num_examples)

    def d_activation_d_Z(
        self,
        Z,
        outputs
    ):
        # Z: (num_outputs, num_examples)
        # outputs: (num_outputs, num_examples)
        # d_activation_d_Z: (num_outputs, num_examples)
        return np.multiply(1.0, Z > 0.0) # (num_outputs, num_examples)
