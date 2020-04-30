from zipfile import ZipFile

from twitter_nlp_toolkit.file_fetcher import file_fetcher
from ..tweet_sentiment_classifier import Classifier, tokenizer_filter

import os
import json
import pickle as pkl
import numpy as np

import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.utils import resample


class LSTM_Model(Classifier):
    """
     LSTM model with trainable embedding layer"
    """

    def __init__(self, max_length=25, vocab_size=1000000, neurons=50,
                 dropout=0.25, rec_dropout=0.25, embed_vec_len=200, activ='hard_sigmoid', optimizer='adam',
                 bootstrap=1, early_stopping=True, patience=50, validation_split=0.2, max_iter=250,
                 batch_size=10000, accuracy=0, remove_punctuation=False, remove_stopwords=False, lemmatize=True,
                 **kwargs):
        """
        Constructor for LSTM classifier using pre-trained embeddings
        Be sure to add additional parametesr to export()
        :param max_length: (int) Maximum text length, ie, number of temporal nodes. Default 25
        :param vocab_size: (int) Maximum vocabulary size. Default 1E7
        :param max_iter: (int) Number of training epochs. Default 100
        :param neurons: (int) Depth (NOT LENGTH) of LSTM network. Default 100
        :param dropout: (float) Dropout
        :param activ: (String) Activation function (for visible layer). Default 'hard_sigmoid'
        :param optimizer: (String) Optimizer. Default 'adam'
        """
        self.type = 'LSTM_Model'
        self.package = 'twitter_nlp_toolkit.tweet_sentiment_classifier.models.lstm_models'
        self.bootstrap = bootstrap
        self.early_stopping = early_stopping
        self.validation_split = validation_split
        self.patience = patience
        self.max_iter = max_iter

        self.max_length = max_length
        self.max_iter = max_iter
        self.batch_size = batch_size
        self.vocab_size = vocab_size
        self.neurons = neurons
        self.dropout = dropout
        self.rec_dropout = rec_dropout
        self.activ = activ
        self.optimizer = optimizer
        self.embed_vec_len = embed_vec_len

        self.remove_punctuation = remove_punctuation
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize

        self.tokenizer = None
        self.classifier = None
        self.word_index = None
        self.embedding_matrix = None
        self.accuracy = accuracy

    def fit(self, train_data, y, weights=None, custom_vocabulary=None):
        """
        :param train_data: (List-like of Strings) Tweets to fit on
        :param y: (Vector) Targets
        :param weights: (Vector) Weights for fitting data
        :param custom_vocabulary: (List of String) Custom vocabulary to use for tokenizer. Not recommended.
        :return: Fit history

        # TODO preprocess custom_vocabulary the reduce memory usage
        """

        if weights is None:
            weights = np.ones(len(y))

        """
        # Preprocess and tokenize text
        """

        if 1 < self.bootstrap < len(y):
            train_data, y, weights = resample(train_data, y, weights, n_samples=self.bootstrap, stratify=y,
                                              replace=False)
        elif self.bootstrap < 1:
            n_samples = int(self.bootstrap * len(y))
            train_data, y, weights = resample(train_data, y, weights, n_samples=n_samples, stratify=y,
                                              replace=False)

        filtered_data = tokenizer_filter(train_data, remove_punctuation=False, remove_stopwords=False,
                                         lemmatize=True, verbose=True)
        print('Filtered data')

        cleaned_data = [' '.join(tweet) for tweet in filtered_data]

        self.tokenizer = Tokenizer(num_words=self.vocab_size, filters='"#$%&()*+-/:;<=>?@[\\]^_`{|}~\t\n')
        self.tokenizer.fit_on_texts(cleaned_data)

        train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

        self.word_index = self.tokenizer.word_index
        print('Found %s unique tokens.' % len(self.word_index))

        X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

        neurons = self.neurons  # Depth (NOT LENGTH) of LSTM network
        dropout = self.dropout  # Dropout - around 0.25 is probably best
        rec_dropout = self.rec_dropout
        activ = self.activ
        costfunction = 'binary_crossentropy'

        """
        Create LSTM model
        """

        print("Creating LSTM model")
        init = tf.keras.initializers.glorot_uniform(seed=1)
        optimizer = self.optimizer

        self.classifier = tf.keras.models.Sequential()

        self.classifier.add(tf.keras.layers.embeddings.Embedding(input_dim=len(self.word_index) + 1,
                                                              output_dim=self.embed_vec_len,
                                                              input_length=self.max_length,
                                                              mask_zero=True,
                                                              embeddings_initializer=keras.initializers.glorot_normal(
                                                                  seed=None)))
        self.classifier.add(tf.keras.layers.SpatialDropout1D(dropout))
        self.classifier.add(tf.keras.layers.LSTM(units=neurons, input_shape=(self.max_length, self.embed_vec_len),
                                              kernel_initializer=init, dropout=dropout,
                                              recurrent_dropout=rec_dropout))
        self.classifier.add(tf.keras.layers.Dense(units=1, kernel_initializer=init, activation=activ))
        self.classifier.compile(loss=costfunction, optimizer=optimizer, metrics=['acc'])
        print(self.classifier.summary())
        es = []
        if self.early_stopping:
            es.append(
                tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=self.patience))

        print('Fitting LSTM model')

        history = self.classifier.fit(X, y, validation_split=self.validation_split, callbacks=es,
                                      batch_size=self.batch_size, sample_weight=weights,
                                      epochs=self.max_iter, verbose=1)

        self.accuracy = np.max(history.history['val_acc'])
        return history

    def refine(self, train_data, y, bootstrap=True, weights=None):
        """
        Train model further

        :param train_data: (list of Strings) Training tweets
        :param y: (vector) Targets
        :param weights: (vector) Training data weights
        :param bootstrap: (bool) Resample training data
        :returns: Fit history
        """

        """
        # Preprocess and tokenize text
        """

        if bootstrap and 1 < self.bootstrap < len(y):
            train_data, y, weights = resample(train_data, y, weights, n_samples=self.bootstrap, stratify=y,
                                              replace=False)
        elif bootstrap and self.bootstrap < 1:
            n_samples = int(self.bootstrap * len(y))
            train_data, y, weights = resample(train_data, y, weights, n_samples=n_samples, stratify=y,
                                              replace=False)

        filtered_data = tokenizer_filter(train_data, remove_punctuation=False, remove_stopwords=False,
                                         lemmatize=True)

        cleaned_data = [' '.join(tweet) for tweet in filtered_data]
        train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

        X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

        es = []
        if self.early_stopping:
            es.append(
                tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=self.patience))

        history = self.classifier.fit(X, y, validation_split=self.validation_split, callbacks=es,
                                      batch_size=self.batch_size, sample_weight=weights,
                                      epochs=self.max_iter, verbose=1)
        self.accuracy = np.max(history.history['val_acc'])
        return history

    def predict(self, data, **kwargs):
        """
        Make binary predictions
        :param data: (list of Strings) Tweets
        :return: (vector of Bool) Predictions
        """
        return np.round(self.predict_proba(data, **kwargs))

    def predict_proba(self, data, preprocess=True):
        """
        Make continuous predictions
        :param data:  (list of Strings) Tweets
        :return: (vector) Predictions
        """
        if self.tokenizer is None:
            raise ValueError('Model has not been trained!')

        filtered_data = tokenizer_filter(data, remove_punctuation=self.remove_punctuation,
                                         remove_stopwords=self.remove_stopwords, lemmatize=self.lemmatize,
                                         verbose=False)

        cleaned_data = [' '.join(tweet) for tweet in filtered_data]
        X = pad_sequences(self.tokenizer.texts_to_sequences(cleaned_data), maxlen=self.max_length)
        return self.classifier.predict(X)

    def export(self, filename):
        """
        Saves the model to disk
        :param filename: (String) Path to file
        """

        parameters = {'Classifier': self.type,
                      'package': self.package,
                      'bootstrap': self.bootstrap,
                      'early_stopping': self.early_stopping,
                      'validation_split': float(self.validation_split),
                      'patience': int(self.patience),
                      'max_iter': int(self.max_iter),
                      'max_length': int(self.max_length),
                      'neurons': int(self.neurons),
                      'dropout': float(self.dropout),
                      'rec_dropout': float(self.rec_dropout),
                      'activ': self.activ,
                      'optimizer': self.optimizer,
                      'vocab_size': self.vocab_size,
                      'batch_size': self.batch_size,
                      'accuracy': float(self.accuracy),
                      'remove_punctuation': self.remove_punctuation,
                      'remove_stopwords': self.remove_stopwords,
                      'lemmatize': self.lemmatize

                      }

        if parameters['bootstrap'] < 1:
            parameters['bootstrap'] = float(parameters['bootstrap'])
        else:
            parameters['bootstrap'] = int(parameters['bootstrap'])

        os.makedirs(filename, exist_ok=True)
        with open(filename + '/param.json', 'w+') as outfile:
            json.dump(parameters, outfile)

        with open(filename + '/lstm_tokenizer.pkl', 'wb+') as outfile:
            pkl.dump(self.tokenizer, outfile)
        model_json = self.classifier.to_json()
        with open(filename + "/lstm_model.json", "w+") as json_file:
            json_file.write(model_json)
        self.classifier.save_weights(filename + "/lstm_model.h5")

    def load_model(self, filename):
        """
        Load a model from the disc
        :param filename: (String) Path to file
        """
        self.tokenizer = pkl.load(open(filename + '/lstm_tokenizer.pkl', 'rb'))
        with open(filename + '/lstm_model.json', 'r') as infile:
            model_json = infile.read()
        self.classifier = tf.keras.models.model_from_json(model_json)
        self.classifier.load_weights(filename + '/lstm_model.h5')
        self.classifier.compile(loss='binary_crossentropy',
                                optimizer=self.optimizer,
                                metrics=['acc'])


class GloVE_Model(Classifier):
    """
    LSTM model that uses GloVE pre-trained embeddings
    # TODO add automatic embedding downloading and unzipping
    """

    def __init__(self, embedding_dict=None, embed_vec_len=200, max_length=25, vocab_size=1000000, batch_size=10000, neurons=100,
                 dropout=0.2, bootstrap=1, early_stopping=True, validation_split=0.2, patience=50, max_iter=250,
                 rec_dropout=0.2, activ='hard_sigmoid', optimizer='adam', accuracy=0, remove_punctuation=False,
                 remove_stopwords=False, lemmatize=True, **kwargs):
        """
        Constructor for LSTM classifier using pre-trained embeddings
        Be sure to add extra parameters to export()
        :param glove_index: (Dict) Embedding index to use. IF not provided, a standard one will be downloaded
        :param name: (String) Name of model
        :param embed_vec_len: (int) Embedding depth. Inferred from dictionary if provided. Otherwise 25, 50, 100, and
        are acceptible values. 200
        :param embedding_dict: (dict) Embedding dictionary
        :param max_length: (int) Maximum text length, ie, number of temporal nodes. Default 25
        :param vocab_size: (int) Maximum vocabulary size. Default 1E7
        :param max_iter: (int) Number of training epochs. Default 100
        :param neurons: (int) Depth (NOT LENGTH) of LSTM network. Default 100
        :param dropout: (float) Dropout
        :param activ: (String) Activation function (for visible layer). Default 'hard_sigmoid'
        :param optimizer: (String) Optimizer. Default 'adam'
        :param early_stopping: (bool) Train with early stopping
        :param validation_split: (float) Fraction of training data to withold for validation
        :param patience: (int) Number of epochs to wait before early stopping
        """
        self.type = 'GloVE_Model'
        self.package = 'twitter_nlp_toolkit.tweet_sentiment_classifier.models.lstm_models'
        self.bootstrap = bootstrap
        self.early_stopping = early_stopping
        self.validation_split = validation_split
        self.patience = patience
        self.max_iter = max_iter
        self.embed_vec_len = embed_vec_len

        self.max_length = max_length
        self.embedding_dict = embedding_dict
        self.max_iter = max_iter
        self.vocab_size = vocab_size
        self.neurons = neurons
        self.dropout = dropout
        self.rec_dropout = rec_dropout
        self.activ = activ
        self.optimizer = optimizer
        self.batch_size = batch_size

        self.remove_punctuation = remove_punctuation
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize

        self.tokenizer = None
        self.classifier = None
        self.word_index = None
        self.embedding_matrix = None
        self.accuracy = accuracy

        if self.embedding_dict is not None:
            self.embed_vec_len = len(list(self.embedding_dict.values())[0])
            print('Setting embedding depth to {}'.format(self.embed_vec_len))

    def fit(self, train_data, y, weights=None, custom_vocabulary=None, clear_embedding_dictionary=True):
        """
        :param train_data: (Dataframe) Training data
        :param y: (vector) Targets
        :param weights: (vector) Weights for fitting data
        :param custom_vocabulary: Custom vocabulary for the tokenizer. Not recommended.
        :param clear_embedding_dictionary: Delete the embedding dictionary after loading the embedding layer.
        Recommended, but will prevent the model from being re-fit (not refined)
        :returns Fit history
        """

        """
        # Preprocess and tokenize text
        """
        if self.embedding_dict is None:
            print('Reloading embedding index')
            try:
                self.embedding_dict = {}
                with open('/.glove_dicts/glove.twitter.27B.' + str(self.embed_vec_len) + 'd.txt', encoding="utf8") as f:
                    for line in f:
                        word, representation = line.split(maxsplit=1)
                        representation = np.fromstring(representation, 'f', sep=' ')
                        self.embedding_dict[word] = representation

                print('Dictionary loaded')

            except FileNotFoundError:
                file_fetcher.download_file("http://nlp.stanford.edu/data/glove.twitter.27B.zip",
                                           "glove_dicts.zip")
                with ZipFile('glove_dicts.zip', 'r') as zipObj:
                    zipObj.extractall(path='/.glove_dicts')
                self.embedding_dict = {}
                with open('/.glove_dicts/glove.twitter.27B.' + str(self.embed_vec_len) + 'd.txt', encoding="utf8") as f:
                    for line in f:
                        word, representation = line.split(maxsplit=1)
                        representation = np.fromstring(representation, 'f', sep=' ')
                        self.embedding_dict[word] = representation

                print('Dictionary loaded')

        if weights is None:
            weights = np.ones(len(y))

        if 1 < self.bootstrap < len(y):
            train_data, y, weights = resample(train_data, y, weights, n_samples=self.bootstrap, stratify=y,
                                              replace=False)
        elif self.bootstrap < 1:
            n_samples = int(self.bootstrap * len(y))
            train_data, y, weights = resample(train_data, y, weights, n_samples=n_samples, stratify=y,
                                              replace=False)

        print('Sampled %d training points' % len(y))

        filtered_data = tokenizer_filter(train_data, remove_punctuation=self.remove_punctuation,
                                         remove_stopwords=self.remove_stopwords, lemmatize=self.lemmatize)
        print('Filtered data')

        cleaned_data = [' '.join(tweet) for tweet in filtered_data]

        if custom_vocabulary is not None:
            print('Applying custom vocabulary')
            self.tokenizer = Tokenizer(num_words=len(custom_vocabulary))
            self.tokenizer.fit_on_texts(custom_vocabulary)
        else:
            print('Fitting tokenizer')
            self.tokenizer = Tokenizer(num_words=self.vocab_size, char_level=False)
            self.tokenizer.fit_on_texts(cleaned_data)

        print(cleaned_data)
        train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

        self.word_index = self.tokenizer.word_index

        X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

        self.embedding_matrix = np.zeros((len(self.word_index) + 1, self.embed_vec_len))
        for word, i in self.word_index.items():
            embedding_vector = self.embedding_dict.get(word)
            if embedding_vector is not None:
                # words not found in embedding index will be all-zeros. # TODO consider optimizing
                self.embedding_matrix[i] = embedding_vector

        neurons = self.neurons  # Depth (NOT LENGTH) of LSTM network
        dropout = self.dropout  # Dropout - around 0.25 is probably best
        rec_dropout = self.rec_dropout
        activ = self.activ
        costfunction = 'binary_crossentropy'

        """
        Create LSTM model
        """

        print("Creating LSTM model")
        init = tf.keras.initializers.glorot_uniform(seed=1)
        optimizer = self.optimizer

        # TODO input_dim is kludged, MUST FIX - should be able to trim embedding matrix in embed_glove.py

        self.classifier = tf.keras.models.Sequential()

        self.classifier.add(tf.keras.layers.embeddings.Embedding(input_dim=len(self.word_index) + 1,
                                                              output_dim=self.embed_vec_len,
                                                              input_length=self.max_length,
                                                              mask_zero=True, trainable=False,
                                                              embeddings_initializer=keras.initializers.Constant(
                                                                  self.embedding_matrix)))
        self.classifier.add(tf.keras.layers.SpatialDropout1D(dropout))
        self.classifier.add(tf.keras.layers.LSTM(units=neurons, input_shape=(self.max_length, self.embed_vec_len),
                                              kernel_initializer=init, dropout=dropout,
                                              recurrent_dropout=rec_dropout))
        self.classifier.add(tf.keras.layers.Dense(units=1, kernel_initializer=init, activation=activ))
        self.classifier.compile(loss=costfunction, optimizer=optimizer, metrics=['acc'])
        print(self.classifier.summary())

        if clear_embedding_dictionary:
            self.embedding_matrix = None
            self.embedding_dict = None

        es = []
        if self.early_stopping:
            es.append(
                tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=self.patience))
        print('Fitting GloVE model')

        history = self.classifier.fit(X, y, validation_split=self.validation_split, batch_size=self.batch_size,
                                      epochs=self.max_iter, sample_weight=weights,
                                      callbacks=es, verbose=1)

        self.accuracy = np.max(history.history['val_acc'])
        return history

    def refine(self, train_data, y, bootstrap=True, weights=None):
        """
        Train model further
        :param train_data: (list of String) Training data
        :param y: (vector) Targets
        :param bootstrap: (bool) Bootstrap resample the refining data. Default True
        :return: Fit history
        """

        if weights is None:
            weights = np.ones(len(y))

        """
        # Preprocess and tokenize text
        """

        if bootstrap and 1 < self.bootstrap < len(y):
            train_data, y, weights = resample(train_data, y, weights, n_samples=self.bootstrap, stratify=y,
                                              replace=False)
        elif bootstrap and self.bootstrap < 1:
            n_samples = int(self.bootstrap * len(y))
            train_data, y, weights = resample(train_data, y, weights, n_samples=n_samples, stratify=y,
                                              replace=False)
        filtered_data = tokenizer_filter(train_data, remove_punctuation=self.remove_punctuation,
                                         remove_stopwords=self.remove_stopwords,
                                         lemmatize=self.lemmatize, verbose=True)
        print('Filtered data')

        cleaned_data = [' '.join(tweet) for tweet in filtered_data]
        train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

        X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

        es = []
        if self.early_stopping:
            es.append(
                tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=self.patience))

        history = self.classifier.fit(X, y, validation_split=self.validation_split, callbacks=es,
                                      batch_size=self.batch_size, sample_weight=weights,
                                      epochs=self.max_iter, verbose=1)
        self.accuracy = np.max(history.history['val_acc'])
        return history

    def predict(self, data, **kwargs):
        """
        Make binary sentiment predictions
        :param data: (List of Strings) Input tweets
        :param kwargs:
        :return: (Vector of Bool) Predictions
        """
        return np.round(self.predict_proba(data, **kwargs))

    def predict_proba(self, data):
        """
        Make continuous sentiment predictions
        :param data: (List of Strings) Input tweets
        :return: (Vector of Float) Predictions
        """
        if self.tokenizer is None:
            raise ValueError('Model has not been trained!')

        filtered_data = tokenizer_filter(data, remove_punctuation=self.remove_punctuation,
                                         remove_stopwords=self.remove_stopwords,
                                         lemmatize=self.lemmatize, verbose=False)

        cleaned_data = [' '.join(tweet) for tweet in filtered_data]
        X = pad_sequences(self.tokenizer.texts_to_sequences(cleaned_data), maxlen=self.max_length)
        return self.classifier.predict(X)

    def export(self, filename):
        """
        Saves the model to disk
        :param filename: (String) Path to file
        """

        parameters = {'Classifier': self.type,
                      'package': self.package,
                      'max_length': int(self.max_length),
                      'neurons': int(self.neurons),
                      'dropout': float(self.dropout),
                      'rec_dropout': float(self.rec_dropout),
                      'activ': self.activ,
                      'optimizer': self.optimizer,
                      'vocab_size': int(self.vocab_size),
                      'max_iter': int(self.max_iter),
                      'batch_size': self.batch_size,
                      'early_stopping': self.early_stopping,
                      'patience': int(self.patience),
                      'bootstrap': self.bootstrap,
                      'validation_split': float(self.validation_split),
                      'accuracy': float(self.accuracy),
                      'remove_punctuation': self.remove_punctuation,
                      'remove_stopwords': self.remove_stopwords,
                      'lemmatize': self.lemmatize
                      }

        if parameters['bootstrap'] < 1:
            parameters['bootstrap'] = float(parameters['bootstrap'])
        else:
            parameters['bootstrap'] = int(parameters['bootstrap'])

        os.makedirs(filename, exist_ok=True)
        with open(filename + '/param.json', 'w+') as outfile:
            json.dump(parameters, outfile)
        with open(filename + '/glove_tokenizer.pkl', 'wb+') as outfile:
            pkl.dump(self.tokenizer, outfile)
        # model_json = self.classifier.to_json()
        with open(filename + "/glove_model.json", "w+") as json_file:
            json_file.write(self.classifier.to_json())
        self.classifier.save_weights(filename + "/glove_model.h5")

    def load_model(self, filename):
        """
        :param filename: (String) Path to file
        """
        self.tokenizer = pkl.load(open(filename + '/glove_tokenizer.pkl', 'rb'))
        with open(filename + '/glove_model.json', 'r') as infile:
            model_json = infile.read()
        self.classifier = tf.keras.models.model_from_json(model_json)
        self.classifier.load_weights(filename + '/glove_model.h5')
        self.classifier.compile(loss='binary_crossentropy',
                                optimizer=self.optimizer,
                                metrics=['acc'])
