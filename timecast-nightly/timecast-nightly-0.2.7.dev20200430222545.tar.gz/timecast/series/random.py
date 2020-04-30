"timecast.series.random"
from typing import Tuple

import jax.numpy as jnp
import numpy as onp


def generate(
    n: int = 1000, loc: float = 0.0, scale: float = 1.0
) -> Tuple[onp.ndarray, onp.ndarray]:
    """
    Description: outputs a timeline randomly distributed i.i.d. from gaussian
    with mean `loc`, standard deviation `scale`
    """
    X = onp.random.normal(loc=loc, scale=scale, size=(n + 1))

    return jnp.asarray(X)[:-1].reshape(-1, 1), jnp.asarray(X)[1:].reshape(-1, 1)
