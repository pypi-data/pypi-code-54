"""timecast.utils.externalize: testing"""
import jax.numpy as jnp
import numpy as onp
import pytest

from timecast.utils import externalize


@pytest.mark.parametrize("shape", [(), (1,), (1, 2, 3)])
def test_externalize_type_error(shape):
    """Test type error"""
    with pytest.raises(TypeError):
        externalize(jnp.ones(shape), dim=1)


def test_externalize_not_jnp_ndarray():
    """Test instance error"""
    with pytest.raises(TypeError):
        externalize(1, dim=1)


@pytest.mark.parametrize("dim", [-2, 3])
def test_externalize_dim_value_error(dim):
    """Test value error"""
    with pytest.raises(ValueError):
        externalize(jnp.ones((1, 1)), dim)


@pytest.mark.parametrize("shape", [(1, 10), (10, 1), (2, 10), (10, 2), (1, 1), (10, 10)])
@pytest.mark.parametrize("dim", [-1, 0, 1, 2])
@pytest.mark.parametrize("was_jax", [True, False])
def test_externalize(shape, dim, was_jax):
    """Test externalize"""
    X = jnp.ones(shape)

    if dim == 2:
        onp.testing.assert_array_equal(X, externalize(X, dim, was_jax))
    elif dim == -1 and len(X.ravel()) == 1:
        assert 1 == externalize(X, dim)
    elif dim == 1 and len(X.ravel()) == 1:
        assert jnp.ones(1) == externalize(X, dim)
    else:
        onp.testing.assert_array_equal(X.squeeze(), externalize(X, dim, was_jax))
