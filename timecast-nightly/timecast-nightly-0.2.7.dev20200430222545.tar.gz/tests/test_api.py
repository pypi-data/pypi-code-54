"""timecacst.api: testing"""
import jax
import numpy as onp

from timecast.api import smap
from timecast.learners import AR
from timecast.learners import PredictLast
from timecast.optim import DummyGrad
from timecast.utils import random


def test_smap_no_objective():
    """Test smap without objective"""
    optimizer_def = DummyGrad(add=4.0)
    model, state = PredictLast.new((1, 10))
    optimizer = optimizer_def.create(model)

    X = jax.random.uniform(random.generate_key(), shape=(5, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(5, 10))
    pred, optimizer, state = smap(X, Y, optimizer)

    onp.testing.assert_array_equal(X, pred)

    # TODO (flax): this will fail once we remove dummy
    assert 20 == optimizer.target.params["dummy"]


def test_smap_state():
    """Test smap with stateful learner"""
    optimizer_def = DummyGrad(add=4.0)
    model, state = AR.new((1, 10), output_dim=1, history_len=1)
    optimizer = optimizer_def.create(model)

    X = jax.random.uniform(random.generate_key(), shape=(5, 10))
    Y = jax.random.uniform(random.generate_key(), shape=(5, 10))
    pred, optimizer, state = smap(X, Y, optimizer, state=state)

    onp.testing.assert_array_equal(state.state["/"]["history"], X[-1, :].reshape(1, -1))
    onp.testing.assert_array_equal(optimizer.target.params["linear"]["bias"], 20.0)
