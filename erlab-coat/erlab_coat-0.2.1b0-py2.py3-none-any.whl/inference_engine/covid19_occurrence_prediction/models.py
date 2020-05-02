__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import pandas
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn
import numpy
from torch.utils.data.dataset import Dataset
from torch.utils.data.dataloader import DataLoader
import torch.nn.utils.rnn
import os, sys
from random import shuffle
from typing import List, Tuple
import torch.optim
from tqdm import tqdm


class COATLSTMPipeline(torch.nn.Module):
    """
    The :class:`COATLSTMPipeline` provides an easy interface to create customizer COAT inference engines for
    covid-19 predictions
    
    Parameters
    ----------
    time_window: `int`, optional (default=15)
        The time window which indicates the number of inputs and outputs to the LSTM

    projected_dynamic_dimension: `int`, optional (default=8)
        The dynamic feature vectors will be mapped to this dimension

    projected_static_dimension: `int`, optional (default=16)
        The static feature vectors will be mapped to this dimension

    hidden_layer_dimension: `int`, optional (default=100)
        The number of hidden layers

    number_of_layers: `int`, optional (default=2)
        The number of LSTM layers

    dropout: `float`, optional (default=0.1)
        The LSTM dropout
    """
    def __init__(self, time_window: int = 15, projected_dynamic_dimension: int = 8,
                 projected_static_dimension: int = 16, hidden_layer_dimension: int = 100, number_of_layers: int = 2,
                 dropout: float = 0.1):
        """
        The constructor
        """
        super(COATLSTMPipeline, self).__init__()
        self.time_window = time_window
        self.hidden_layer_dimension = hidden_layer_dimension
        self.projected_dynamic_dimension = projected_dynamic_dimension
        self.projected_static_dimension = projected_static_dimension
        self.number_of_layers = number_of_layers

        self.fc_static_projection = torch.nn.Linear(89, projected_static_dimension)
        self.fc_dynamic_projection = torch.nn.Linear(25, projected_dynamic_dimension)
        self.fc_output_projection = torch.nn.Linear(hidden_layer_dimension + projected_static_dimension, 1)
        self.rnn = torch.nn.LSTM(projected_dynamic_dimension, hidden_layer_dimension, num_layers=number_of_layers,
                                 batch_first=True, dropout=dropout, bidirectional=False, bias=True)
        self.loss = torch.nn.MSELoss()

    def forward(self, static_feature_vectors: torch.Tensor, dynamic_feature_vector_sequences: torch.Tensor, target_sequences: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        The forward pass helper

        Parameters
        ----------
        static_feature_vectors: `torch.Tensor`, required
            The static feature vectors of shape:
            ```
            >> static_feature_vectors.shape
            (batch_size, 89)
            ```

        dynamic_feature_vector_sequences: `torch.Tensor`, required
            The dynamic feature vectors of shape:
            ```
            >> static_feature_vectors.shape
            (batch_size, time_window*2, 25)
            ```

        target_sequences: `torch.Tensor`, required
            The elements of shape:
            ```
            >> target_sequences.shape
            (batch_size, timewindow * 2)
            ```

        Returns
        ----------
        The `Tuple[torch.Tensor, torch.Tensor, torch.Tensor]`
        """
        dynamic_feature_vector_sequences = self.fc_dynamic_projection(dynamic_feature_vector_sequences)
        dynamic_feature_vector_sequences = dynamic_feature_vector_sequences[:, :self.time_window, :]
        target_sequences = target_sequences[:, self.time_window:]
        static_feature_vectors = self.fc_static_projection(static_feature_vectors)

        initial_hidden_state = torch.zeros(self.number_of_layers, static_feature_vectors.shape[0],
                                           self.hidden_layer_dimension)
        initial_cell_state = torch.zeros(self.number_of_layers, static_feature_vectors.shape[0],
                                         self.hidden_layer_dimension)
        lstm_activations, _ = self.rnn(dynamic_feature_vector_sequences, (initial_hidden_state, initial_cell_state))
        outputs = self.fc_output_projection(
            torch.cat((lstm_activations, static_feature_vectors.unsqueeze(1).repeat(1, self.time_window, 1)), dim=2))
        loss = 100.0 * self.loss(outputs.squeeze(), target_sequences)
        return loss, outputs, target_sequences
