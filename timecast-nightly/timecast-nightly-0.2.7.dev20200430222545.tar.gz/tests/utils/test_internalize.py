"""timecast.utils.internalize: testing"""
import jax.numpy as jnp
import numpy as onp
import pytest

from timecast.utils import internalize


@pytest.mark.parametrize(
    "n,shape,expected",
    [
        (1, (1,), (True, 1)),
        (1, (10,), (False, jnp.ones((10, 1)))),
        (1, (1, 1), (True, 1)),
        (1, (10, 1), (False, jnp.ones((10, 1)))),
        (2, (2,), (True, jnp.ones((1, 2)))),
        (2, (1, 2), (True, jnp.ones((1, 2)))),
        (2, (4, 2), (False, jnp.ones((4, 2)))),
        (1, (), (True, 1)),
    ],
)
def test_internalize(n, shape, expected):
    """Test internalize"""
    X = jnp.ones(shape)

    X, is_value, dim, _ = internalize(X, n)

    assert is_value == expected[0]
    onp.testing.assert_array_equal(X, expected[1])


@pytest.mark.parametrize(
    "n,shape",
    [(2, (1, 3)), (2, (3, 1)), (2, (2, 4)), (2, (2, 1)), (2, (5,)), (1, (2, 2)), (1, (1, 10))],
)
def test_internalize_value_error(n, shape):
    """Test value error"""
    with pytest.raises(ValueError):
        internalize(jnp.ones(shape), n)


def test_internalize_type_error():
    """Test type error"""
    with pytest.raises(TypeError):
        internalize(jnp.ones((1, 2, 3)), 10)


@pytest.mark.parametrize("n,expected", [(1, True), (10, False)])
def test_internalize_scalar(n, expected):
    """Test scalar"""
    if expected:
        _, is_value, _, _ = internalize(4, n)
        assert is_value == expected
    else:
        with pytest.raises(ValueError):
            internalize(4, n)
