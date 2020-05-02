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
from typing import List, Tuple, Any
import torch.optim
from tqdm import tqdm
from erlab_coat.inference_engine.covid19_occurrence_prediction.data import OliviaCovidOccurrencePredictionDataset
from erlab_coat.inference_engine.covid19_occurrence_prediction.models import COATLSTMPipeline


def train_coat_covid19_predictor(
        optimizer: Any,
        model: torch.nn.Module,
        train_dataset: OliviaCovidOccurrencePredictionDataset,
        test_dataset: OliviaCovidOccurrencePredictionDataset,
        max_epochs: int = 15,
        batch_size: int = 64,
) -> Tuple[List[numpy.ndarray], List[numpy.ndarray], List[numpy.ndarray], List[List[str]]]:

    static_scaler, dynamic_scaler, target_scaler = train_dataset.get_minmax_scalers()
    test_dataset.apply_minmax_scalers(static_scaler, dynamic_scaler, target_scaler)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    epoch_loss_sequences = {
        'train': [],
        'test': []
    }

    for epoch in range(max_epochs):
        train_dataloader_tqdm = tqdm(train_dataloader)
        test_dataloader_tqdm = tqdm(test_dataloader)
        print("-> epoch: %d\n" % epoch)
        loss_sequence = []
        for batch in train_dataloader_tqdm:
            optimizer.zero_grad()
            loss, _, _ = model(batch[0].float(), batch[1].float(), batch[2].float())
            loss_sequence.append(loss.item())
            loss.backward()
            optimizer.step()
            train_dataloader_tqdm.set_description("(training): minibatch loss:{:.4f}".format(loss.item()))
            train_dataloader_tqdm.refresh()
        print("train loss: {:.4f}".format(numpy.mean(loss_sequence)))
        epoch_loss_sequences['train'].append(numpy.mean(loss_sequence))

        test_loss_sequence = []
        test_outputs = []
        test_targets = []
        test_locations = []
        for batch in test_dataloader_tqdm:
            test_locations.append(batch[3])
            loss, outputs, target_sequences = model(batch[0].float(), batch[1].float(), batch[2].float())
            test_outputs.append(outputs.data.cpu().numpy())
            test_targets.append(target_sequences.data.cpu().numpy())
            test_loss_sequence.append(loss.item())
            test_dataloader_tqdm.set_description("(testing): minibatch loss:{:.4f}".format(loss.item()))
            test_dataloader_tqdm.refresh()
        print("test loss: {:.4f}".format(numpy.mean(test_loss_sequence)))
        epoch_loss_sequences['test'].append(numpy.mean(test_loss_sequence))

    return epoch_loss_sequences, test_loss_sequence, test_outputs, test_targets, test_locations
