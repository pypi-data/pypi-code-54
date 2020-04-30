import six
import os
import time
import logging
import tensorflow as tf

from eight_mile.confusion import ConfusionMatrix
from eight_mile.utils import listify
from eight_mile.tf.optz import optimizer

from baseline.utils import get_model_file, get_metric_cmp
from baseline.tf.tfy import _add_ema, TRAIN_FLAG, SET_TRAIN_FLAG
from baseline.tf.classify.training.utils import to_tensors
from baseline.progress import create_progress_bar
from baseline.train import EpochReportingTrainer, create_trainer, register_trainer, register_training_func
from baseline.utils import verbose_output
from baseline.model import create_model_for
import numpy as np

# Number of batches to prefetch if using tf.datasets
NUM_PREFETCH = 2
# The shuffle buffer
SHUF_BUF_SZ = 5000

log = logging.getLogger('baseline.timing')


@register_training_func('classify')
def fit_datasets(model_params, ts, vs, es=None, **kwargs):
    """
    Train a classifier using TensorFlow with `tf.dataset`.  This
    is the default behavior for training.

    :param model_params: The model (or parameters to create the model) to train
    :param ts: A training data set
    :param vs: A validation data set
    :param es: A test data set, can be None
    :param kwargs:
        See below

    :Keyword Arguments:
        * *do_early_stopping* (``bool``) --
          Stop after evaluation data is no longer improving.  Defaults to True
        * *verbose* (`dict`) A dictionary containing `console` boolean and `file` name if on
        * *epochs* (``int``) -- how many epochs.  Default to 20
        * *outfile* -- Model output file, defaults to classifier-model.pyth
        * *patience* --
           How many epochs where evaluation is no longer improving before we give up
        * *reporting* --
           Callbacks which may be used on reporting updates
        * *nsteps* (`int`) -- If we should report every n-steps, this should be passed
        * *ema_decay* (`float`) -- If we are doing an exponential moving average, what decay to us4e
        * *clip* (`int`) -- If we are doing gradient clipping, what value to use
        * *optim* (`str`) -- The name of the optimizer we are using
        * *lr* (`float`) -- The learning rate we are using
        * *mom* (`float`) -- If we are using SGD, what value to use for momentum
        * *beta1* (`float`) -- Adam-specific hyper-param, defaults to `0.9`
        * *beta2* (`float`) -- Adam-specific hyper-param, defaults to `0.999`
        * *epsilon* (`float`) -- Adam-specific hyper-param, defaults to `1e-8

    :return: None
    """
    do_early_stopping = bool(kwargs.get('do_early_stopping', True))
    verbose = kwargs.get('verbose', {'console': kwargs.get('verbose_console', False), 'file': kwargs.get('verbose_file', None)})
    epochs = int(kwargs.get('epochs', 20))
    model_file = get_model_file('classify', 'tf', kwargs.get('basedir'))

    batchsz = kwargs['batchsz']
    lengths_key = model_params.get('lengths_key')

    ## First, make tf.datasets for ts, vs and es
    # https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/distribute/README.md
    # effective_batch_sz = args.batchsz*args.gpus
    test_batchsz = kwargs.get('test_batchsz', batchsz)
    train_dataset = tf.data.Dataset.from_tensor_slices(to_tensors(ts, lengths_key))
    train_dataset = train_dataset.shuffle(buffer_size=SHUF_BUF_SZ)
    train_dataset = train_dataset.batch(batchsz, drop_remainder=False)
    train_dataset = train_dataset.repeat(epochs + 1)
    train_dataset = train_dataset.prefetch(NUM_PREFETCH)

    valid_dataset = tf.data.Dataset.from_tensor_slices(to_tensors(vs, lengths_key))
    valid_dataset = valid_dataset.batch(batchsz, drop_remainder=False)
    valid_dataset = valid_dataset.repeat(epochs + 1)
    valid_dataset = valid_dataset.prefetch(NUM_PREFETCH)

    test_dataset = tf.data.Dataset.from_tensor_slices(to_tensors(es, lengths_key))
    test_dataset = test_dataset.batch(test_batchsz, drop_remainder=False)
    test_dataset = test_dataset.repeat(epochs + 1)
    test_dataset = test_dataset.prefetch(NUM_PREFETCH)

    iter = tf.compat.v1.data.Iterator.from_structure(tf.compat.v1.data.get_output_types(train_dataset),
                                                     tf.compat.v1.data.get_output_shapes(train_dataset))

    features, y = iter.get_next()
    # Add features to the model params
    model_params.update(features)
    model_params['y'] = tf.one_hot(tf.reshape(y, [-1]), len(model_params['labels']))
    # create the initialisation operations
    train_init_op = iter.make_initializer(train_dataset)
    valid_init_op = iter.make_initializer(valid_dataset)
    test_init_op = iter.make_initializer(test_dataset)

    ema = True if kwargs.get('ema_decay') is not None else False

    best_metric = 0
    if do_early_stopping:
        early_stopping_metric = kwargs.get('early_stopping_metric', 'acc')
        early_stopping_cmp, best_metric = get_metric_cmp(early_stopping_metric, kwargs.get('early_stopping_cmp'))
        patience = kwargs.get('patience', epochs)
        print('Doing early stopping on [%s] with patience [%d]' % (early_stopping_metric, patience))

    reporting_fns = listify(kwargs.get('reporting', []))
    print('reporting', reporting_fns)

    TRAIN_FLAG()
    trainer = create_trainer(model_params, **kwargs)
    last_improved = 0

    for epoch in range(epochs):
        trainer.sess.run(train_init_op)
        trainer.train(ts, reporting_fns)
        trainer.sess.run(valid_init_op)
        test_metrics = trainer.test(vs, reporting_fns, phase='Valid')

        if do_early_stopping is False:
            trainer.checkpoint()
            trainer.model.save(model_file)

        elif early_stopping_cmp(test_metrics[early_stopping_metric], best_metric):
            last_improved = epoch
            best_metric = test_metrics[early_stopping_metric]
            print('New best %.3f' % best_metric)
            trainer.checkpoint()
            trainer.model.save(model_file)

        elif (epoch - last_improved) > patience:
            print('Stopping due to persistent failures to improve')
            break

    if do_early_stopping is True:
        print('Best performance on %s: %.3f at epoch %d' % (early_stopping_metric, best_metric, last_improved))

    if es is not None:
        print('Reloading best checkpoint')
        trainer.recover_last_checkpoint()
        trainer.sess.run(test_init_op)
        trainer.test(es, reporting_fns, phase='Test', verbose=verbose)
