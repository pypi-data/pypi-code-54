import numpy as np

class Linear(object):
    def __init__(self, a, b, c, d):
        self._matrix_a = a
        self._matrix_b = b
        self._matrix_c = c
        self._matrix_d = d
        self._dt = 0.02
        self._num_states, self._num_inputs = self._matrix_b.shape
        self._num_outputs, _ = self._matrix_c.shape
        self._state = np.zeros((self._num_states,1))
        self._x_temp = np.zeros((self._num_states,1))
    def reset(self):
        self._state = np.zeros((self._num_states,1))
        self._x_temp = np.zeros((self._num_states,1))
    def step(self, action):
        x = self._state
        u = action.reshape(self._num_inputs,1)
        
        x_dot = np.dot(self._matrix_a, x) + np.dot(self._matrix_b, u)
        y = np.dot(self._matrix_c, x) + np.dot(self._matrix_d, u)
        next_x = self._x_temp + self._dt * x_dot

        self._state = next_x
        self._x_temp = next_x
        return self._state.flatten()