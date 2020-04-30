# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from contextlib import contextmanager
import functools
import re
import itertools as it
import os
from typing import Dict, Sequence, Union
import sys
import unittest
import warnings

from absl.testing import absltest
from absl.testing import parameterized

import numpy as onp
import numpy.random as npr
import scipy

from . import api
from . import core
from . import dtypes
from . import lax
from .config import flags, bool_env
from .util import partial
from .tree_util import tree_multimap, tree_all, tree_map, tree_reduce
from .lib import xla_bridge
from .interpreters import xla


FLAGS = flags.FLAGS
flags.DEFINE_enum(
    'jax_test_dut', '',
    enum_values=['', 'cpu', 'gpu', 'tpu'],
    help=
    'Describes the device under test in case special consideration is required.'
)

flags.DEFINE_integer(
  'num_generated_cases',
  int(os.getenv('JAX_NUM_GENERATED_CASES', 10)),
  help='Number of generated cases to test')

flags.DEFINE_bool(
    'jax_skip_slow_tests',
    bool_env('JAX_SKIP_SLOW_TESTS', False),
    help=
    'Skip tests marked as slow (> 5 sec).'
)

EPS = 1e-4

def _dtype(x):
  return (getattr(x, 'dtype', None) or
          onp.dtype(dtypes.python_scalar_dtypes.get(type(x), None)) or
          onp.asarray(x).dtype)

def is_sequence(x):
  try:
    iter(x)
  except TypeError:
    return False
  else:
    return True

_default_tolerance = {
  onp.dtype(onp.bool_): 0,
  onp.dtype(onp.int8): 0,
  onp.dtype(onp.int16): 0,
  onp.dtype(onp.int32): 0,
  onp.dtype(onp.int64): 0,
  onp.dtype(onp.uint8): 0,
  onp.dtype(onp.uint16): 0,
  onp.dtype(onp.uint32): 0,
  onp.dtype(onp.uint64): 0,
  onp.dtype(dtypes.bfloat16): 1e-2,
  onp.dtype(onp.float16): 1e-3,
  onp.dtype(onp.float32): 1e-6,
  onp.dtype(onp.float64): 1e-15,
  onp.dtype(onp.complex64): 1e-6,
  onp.dtype(onp.complex128): 1e-15,
}

def default_tolerance():
  if device_under_test() != "tpu":
    return _default_tolerance
  tol = _default_tolerance.copy()
  tol[onp.dtype(onp.float32)] = 1e-3
  tol[onp.dtype(onp.complex64)] = 1e-3
  return tol

default_gradient_tolerance = {
  onp.dtype(dtypes.bfloat16): 1e-1,
  onp.dtype(onp.float16): 1e-2,
  onp.dtype(onp.float32): 2e-3,
  onp.dtype(onp.float64): 1e-5,
  onp.dtype(onp.complex64): 1e-3,
  onp.dtype(onp.complex128): 1e-5,
}

def _assert_numpy_allclose(a, b, atol=None, rtol=None):
  a = a.astype(onp.float32) if a.dtype == dtypes.bfloat16 else a
  b = b.astype(onp.float32) if b.dtype == dtypes.bfloat16 else b
  kw = {}
  if atol: kw["atol"] = atol
  if rtol: kw["rtol"] = rtol
  onp.testing.assert_allclose(a, b, **kw)

def tolerance(dtype, tol=None):
  tol = {} if tol is None else tol
  if not isinstance(tol, dict):
    return tol
  tol = {onp.dtype(key): value for key, value in tol.items()}
  dtype = dtypes.canonicalize_dtype(onp.dtype(dtype))
  return tol.get(dtype, default_tolerance()[dtype])

def _normalize_tolerance(tol):
  tol = tol or 0
  if isinstance(tol, dict):
    return {onp.dtype(k): v for k, v in tol.items()}
  else:
    return {k: tol for k in _default_tolerance.keys()}

def join_tolerance(tol1, tol2):
  tol1 = _normalize_tolerance(tol1)
  tol2 = _normalize_tolerance(tol2)
  out = tol1
  for k, v in tol2.items():
    out[k] = max(v, tol1.get(k, 0))
  return out

def _assert_numpy_close(a, b, atol=None, rtol=None):
  assert a.shape == b.shape
  atol = max(tolerance(a.dtype, atol), tolerance(b.dtype, atol))
  rtol = max(tolerance(a.dtype, rtol), tolerance(b.dtype, rtol))
  _assert_numpy_allclose(a, b, atol=atol * a.size, rtol=rtol * b.size)


def check_eq(xs, ys):
  tree_all(tree_multimap(_assert_numpy_allclose, xs, ys))


def check_close(xs, ys, atol=None, rtol=None):
  assert_close = partial(_assert_numpy_close, atol=atol, rtol=rtol)
  tree_all(tree_multimap(assert_close, xs, ys))


def inner_prod(xs, ys):
  def contract(x, y):
    return onp.real(onp.dot(onp.conj(x).reshape(-1), y.reshape(-1)))
  return tree_reduce(onp.add, tree_multimap(contract, xs, ys))


add = partial(tree_multimap, lambda x, y: onp.add(x, y, dtype=_dtype(x)))
sub = partial(tree_multimap, lambda x, y: onp.subtract(x, y, dtype=_dtype(x)))
conj = partial(tree_map, lambda x: onp.conj(x, dtype=_dtype(x)))

def scalar_mul(xs, a):
  return tree_map(lambda x: onp.multiply(x, a, dtype=_dtype(x)), xs)


def rand_like(rng, x):
  shape = onp.shape(x)
  dtype = _dtype(x)
  randn = lambda: onp.asarray(rng.randn(*shape), dtype=dtype)
  if dtypes.issubdtype(dtype, onp.complexfloating):
    return randn() + dtype.type(1.0j) * randn()
  else:
    return randn()


def numerical_jvp(f, primals, tangents, eps=EPS):
  delta = scalar_mul(tangents, eps)
  f_pos = f(*add(primals, delta))
  f_neg = f(*sub(primals, delta))
  return scalar_mul(sub(f_pos, f_neg), 0.5 / eps)


def _merge_tolerance(tol, default):
  if tol is None:
    return default
  if not isinstance(tol, dict):
    return tol
  out = default.copy()
  for k, v in tol.items():
    out[onp.dtype(k)] = v
  return out

def check_jvp(f, f_jvp, args, atol=None, rtol=None, eps=EPS):
  atol = _merge_tolerance(atol, default_gradient_tolerance)
  rtol = _merge_tolerance(rtol, default_gradient_tolerance)
  rng = onp.random.RandomState(0)
  tangent = tree_map(partial(rand_like, rng), args)
  v_out, t_out = f_jvp(args, tangent)
  v_out_expected = f(*args)
  t_out_expected = numerical_jvp(f, args, tangent, eps=eps)
  # In principle we should expect exact equality of v_out and v_out_expected,
  # but due to nondeterminism especially on GPU (e.g., due to convolution
  # autotuning) we only require "close".
  check_close(v_out, v_out_expected, atol=atol, rtol=rtol)
  check_close(t_out, t_out_expected, atol=atol, rtol=rtol)


def check_vjp(f, f_vjp, args, atol=None, rtol=None, eps=EPS):
  atol = _merge_tolerance(atol, default_gradient_tolerance)
  rtol = _merge_tolerance(rtol, default_gradient_tolerance)
  _rand_like = partial(rand_like, onp.random.RandomState(0))
  v_out, vjpfun = f_vjp(*args)
  v_out_expected = f(*args)
  check_close(v_out, v_out_expected, atol=atol, rtol=rtol)
  tangent = tree_map(_rand_like, args)
  tangent_out = numerical_jvp(f, args, tangent, eps=eps)
  cotangent = tree_map(_rand_like, v_out)
  cotangent_out = conj(vjpfun(conj(cotangent)))
  ip = inner_prod(tangent, cotangent_out)
  ip_expected = inner_prod(tangent_out, cotangent)
  check_close(ip, ip_expected, atol=atol, rtol=rtol)


def check_grads(f, args, order,
                modes=["fwd", "rev"], atol=None, rtol=None, eps=None):
  """Check gradients from automatic differentiation against finite differences.

  Gradients are only checked in a single randomly chosen direction, which
  ensures that the finite difference calculation does not become prohibitively
  expensive even for large input/output spaces.

  Args:
    f: function to check at ``f(*args)``.
    args: tuple of argument values.
    order: forward and backwards gradients up to this order are checked.
    modes: lists of gradient modes to check ('fwd' and/or 'rev').
    atol: absolute tolerance for gradient equality.
    rtol: relative tolerance for gradient equality.
    eps: step size used for finite differences.

  Raises:
    AssertionError: if gradients do not match.
  """
  args = tuple(args)
  eps = eps or EPS

  _check_jvp = partial(check_jvp, atol=atol, rtol=rtol, eps=eps)
  _check_vjp = partial(check_vjp, atol=atol, rtol=rtol, eps=eps)

  def _check_grads(f, args, order):
    if "fwd" in modes:
      _check_jvp(f, partial(api.jvp, f), args)
      if order > 1:
        _check_grads(partial(api.jvp, f), (args, args), order - 1)

    if "rev" in modes:
      _check_vjp(f, partial(api.vjp, f), args)
      if order > 1:
        def f_vjp(*args):
          out_primal_py, vjp_py = api.vjp(f, *args)
          return vjp_py(out_primal_py)
        _check_grads(f_vjp, args, order - 1)

  _check_grads(f, args, order)


@contextmanager
def count_primitive_compiles():
  xla.xla_primitive_callable.cache_clear()

  # We count how many times we call primitive_computation (which is called
  # inside xla_primitive_callable) instead of xla_primitive_callable so we don't
  # count cache hits.
  primitive_computation = xla.primitive_computation
  count = [0]

  def primitive_computation_and_count(*args, **kwargs):
    count[0] += 1
    return primitive_computation(*args, **kwargs)

  xla.primitive_computation = primitive_computation_and_count
  try:
    yield count
  finally:
    xla.primitive_computation = primitive_computation


@contextmanager
def count_jit_and_pmap_compiles():
  # No need to clear any caches since we generally jit and pmap fresh callables
  # in tests.

  jaxpr_subcomp = xla.jaxpr_subcomp
  count = [0]

  def jaxpr_subcomp_and_count(*args, **kwargs):
    count[0] += 1
    return jaxpr_subcomp(*args, **kwargs)

  xla.jaxpr_subcomp = jaxpr_subcomp_and_count
  try:
    yield count
  finally:
    xla.jaxpr_subcomp = jaxpr_subcomp


def device_under_test():
  return FLAGS.jax_test_dut or xla_bridge.get_backend().platform

def if_device_under_test(device_type: Union[str, Sequence[str]],
                         if_true, if_false):
  """Chooses `if_true` of `if_false` based on device_under_test."""
  if device_under_test() in ([device_type] if isinstance(device_type, str)
                             else device_type):
    return if_true
  else:
    return if_false

def supported_dtypes():
  if device_under_test() == "tpu":
    return {onp.bool_, onp.int32, onp.uint32, dtypes.bfloat16, onp.float32,
            onp.complex64}
  else:
    return {onp.bool_, onp.int8, onp.int16, onp.int32, onp.int64,
            onp.uint8, onp.uint16, onp.uint32, onp.uint64,
            dtypes.bfloat16, onp.float16, onp.float32, onp.float64,
            onp.complex64, onp.complex128}

def skip_if_unsupported_type(dtype):
  if dtype not in supported_dtypes():
    raise unittest.SkipTest(
      f"Type {dtype} not supported on {device_under_test()}")

def skip_on_devices(*disabled_devices):
  """A decorator for test methods to skip the test on certain devices."""
  def skip(test_method):
    @functools.wraps(test_method)
    def test_method_wrapper(self, *args, **kwargs):
      device = device_under_test()
      if device in disabled_devices:
        test_name = getattr(test_method, '__name__', '[unknown test]')
        raise unittest.SkipTest(
          f"{test_name} not supported on {device.upper()}.")
      return test_method(self, *args, **kwargs)
    return test_method_wrapper
  return skip


def skip_on_flag(flag_name, skip_value):
  """A decorator for test methods to skip the test when flags are set."""
  def skip(test_method):        # pylint: disable=missing-docstring
    @functools.wraps(test_method)
    def test_method_wrapper(self, *args, **kwargs):
      flag_value = getattr(FLAGS, flag_name)
      if flag_value == skip_value:
        test_name = getattr(test_method, '__name__', '[unknown test]')
        raise unittest.SkipTest(
          f"{test_name} not supported when FLAGS.{flag_name} is {flag_value}")
      return test_method(self, *args, **kwargs)
    return test_method_wrapper
  return skip

# TODO(phawkins): bug https://github.com/google/jax/issues/432
skip_on_mac_linalg_bug = partial(
  unittest.skipIf,
  sys.platform == "darwin" and scipy.version.version > "1.1.0",
  "Test fails on Mac with new scipy (issue #432)")


def format_test_name_suffix(opname, shapes, dtypes):
  arg_descriptions = (format_shape_dtype_string(shape, dtype)
                      for shape, dtype in zip(shapes, dtypes))
  return '{}_{}'.format(opname.capitalize(), '_'.join(arg_descriptions))


# We use special symbols, represented as singleton objects, to distinguish
# between NumPy scalars, Python scalars, and 0-D arrays.
class ScalarShape(object):
  def __len__(self): return 0
class _NumpyScalar(ScalarShape): pass
class _PythonScalar(ScalarShape): pass
NUMPY_SCALAR_SHAPE = _NumpyScalar()
PYTHON_SCALAR_SHAPE = _PythonScalar()


def _dims_of_shape(shape):
  """Converts `shape` to a tuple of dimensions."""
  if type(shape) in (list, tuple):
    return shape
  elif isinstance(shape, ScalarShape):
    return ()
  else:
    raise TypeError(type(shape))


def _cast_to_shape(value, shape, dtype):
  """Casts `value` to the correct Python type for `shape` and `dtype`."""
  if shape is NUMPY_SCALAR_SHAPE:
    # explicitly cast to NumPy scalar in case `value` is a Python scalar.
    return onp.dtype(dtype).type(value)
  elif shape is PYTHON_SCALAR_SHAPE:
    # explicitly cast to Python scalar via https://stackoverflow.com/a/11389998
    return onp.asarray(value).item()
  elif type(shape) in (list, tuple):
    assert onp.shape(value) == tuple(shape)
    return value
  else:
    raise TypeError(type(shape))


def dtype_str(dtype):
  return onp.dtype(dtype).name


def format_shape_dtype_string(shape, dtype):
  if shape is NUMPY_SCALAR_SHAPE:
    return dtype_str(dtype)
  elif shape is PYTHON_SCALAR_SHAPE:
    return 'py' + dtype_str(dtype)
  elif type(shape) in (list, tuple):
    shapestr = ','.join(str(dim) for dim in shape)
    return '{}[{}]'.format(dtype_str(dtype), shapestr)
  elif type(shape) is int:
    return '{}[{},]'.format(dtype_str(dtype), shape)
  elif isinstance(shape, onp.ndarray):
    return '{}[{}]'.format(dtype_str(dtype), shape)
  else:
    raise TypeError(type(shape))


def _rand_dtype(rand, shape, dtype, scale=1., post=lambda x: x):
  """Produce random values given shape, dtype, scale, and post-processor.

  Args:
    rand: a function for producing random values of a given shape, e.g. a
      bound version of either onp.RandomState.randn or onp.RandomState.rand.
    shape: a shape value as a tuple of positive integers.
    dtype: a numpy dtype.
    scale: optional, a multiplicative scale for the random values (default 1).
    post: optional, a callable for post-processing the random values (default
      identity).

  Returns:
    An ndarray of the given shape and dtype using random values based on a call
    to rand but scaled, converted to the appropriate dtype, and post-processed.
  """
  r = lambda: onp.asarray(scale * rand(*_dims_of_shape(shape)), dtype)
  if dtypes.issubdtype(dtype, onp.complexfloating):
    vals = r() + 1.0j * r()
  else:
    vals = r()
  return _cast_to_shape(onp.asarray(post(vals), dtype), shape, dtype)


def rand_default(scale=3):
  randn = npr.RandomState(0).randn
  return partial(_rand_dtype, randn, scale=scale)


def rand_nonzero():
  post = lambda x: onp.where(x == 0, onp.array(1, dtype=x.dtype), x)
  randn = npr.RandomState(0).randn
  return partial(_rand_dtype, randn, scale=3, post=post)


def rand_positive():
  post = lambda x: x + 1
  rand = npr.RandomState(0).rand
  return partial(_rand_dtype, rand, scale=2, post=post)


def rand_small():
  randn = npr.RandomState(0).randn
  return partial(_rand_dtype, randn, scale=1e-3)


def rand_not_small(offset=10.):
  post = lambda x: x + onp.where(x > 0, offset, -offset)
  randn = npr.RandomState(0).randn
  return partial(_rand_dtype, randn, scale=3., post=post)


def rand_small_positive():
  rand = npr.RandomState(0).rand
  return partial(_rand_dtype, rand, scale=2e-5)

def rand_uniform(low=0.0, high=1.0):
  assert low < high
  rand = npr.RandomState(0).rand
  post = lambda x: x * (high - low) + low
  return partial(_rand_dtype, rand, post=post)


def rand_some_equal():
  randn = npr.RandomState(0).randn
  rng = npr.RandomState(0)

  def post(x):
    x_ravel = x.ravel()
    if len(x_ravel) == 0:
      return x
    flips = rng.rand(*onp.shape(x)) < 0.5
    return onp.where(flips, x_ravel[0], x)

  return partial(_rand_dtype, randn, scale=100., post=post)


def rand_some_inf():
  """Return a random sampler that produces infinities in floating types."""
  rng = npr.RandomState(1)
  base_rand = rand_default()

  """
  TODO: Complex numbers are not correctly tested
  If blocks should be switched in order, and relevant tests should be fixed
  """
  def rand(shape, dtype):
    """The random sampler function."""
    if not dtypes.issubdtype(dtype, onp.floating):
      # only float types have inf
      return base_rand(shape, dtype)

    if dtypes.issubdtype(dtype, onp.complexfloating):
      base_dtype = onp.real(onp.array(0, dtype=dtype)).dtype
      out = (rand(shape, base_dtype) +
             onp.array(1j, dtype) * rand(shape, base_dtype))
      return _cast_to_shape(out, shape, dtype)

    dims = _dims_of_shape(shape)
    posinf_flips = rng.rand(*dims) < 0.1
    neginf_flips = rng.rand(*dims) < 0.1

    vals = base_rand(shape, dtype)
    vals = onp.where(posinf_flips, onp.array(onp.inf, dtype=dtype), vals)
    vals = onp.where(neginf_flips, onp.array(-onp.inf, dtype=dtype), vals)

    return _cast_to_shape(onp.asarray(vals, dtype=dtype), shape, dtype)

  return rand

def rand_some_nan():
  """Return a random sampler that produces nans in floating types."""
  rng = npr.RandomState(1)
  base_rand = rand_default()

  def rand(shape, dtype):
    """The random sampler function."""
    if dtypes.issubdtype(dtype, onp.complexfloating):
      base_dtype = onp.real(onp.array(0, dtype=dtype)).dtype
      out = (rand(shape, base_dtype) +
             onp.array(1j, dtype) * rand(shape, base_dtype))
      return _cast_to_shape(out, shape, dtype)

    if not dtypes.issubdtype(dtype, onp.floating):
      # only float types have inf
      return base_rand(shape, dtype)

    dims = _dims_of_shape(shape)
    nan_flips = rng.rand(*dims) < 0.1

    vals = base_rand(shape, dtype)
    vals = onp.where(nan_flips, onp.array(onp.nan, dtype=dtype), vals)

    return _cast_to_shape(onp.asarray(vals, dtype=dtype), shape, dtype)

  return rand

def rand_some_inf_and_nan():
  """Return a random sampler that produces infinities in floating types."""
  rng = npr.RandomState(1)
  base_rand = rand_default()

  """
  TODO: Complex numbers are not correctly tested
  If blocks should be switched in order, and relevant tests should be fixed
  """
  def rand(shape, dtype):
    """The random sampler function."""
    if not dtypes.issubdtype(dtype, onp.floating):
      # only float types have inf
      return base_rand(shape, dtype)

    if dtypes.issubdtype(dtype, onp.complexfloating):
      base_dtype = onp.real(onp.array(0, dtype=dtype)).dtype
      out = (rand(shape, base_dtype) +
             onp.array(1j, dtype) * rand(shape, base_dtype))
      return _cast_to_shape(out, shape, dtype)

    dims = _dims_of_shape(shape)
    posinf_flips = rng.rand(*dims) < 0.1
    neginf_flips = rng.rand(*dims) < 0.1
    nan_flips = rng.rand(*dims) < 0.1

    vals = base_rand(shape, dtype)
    vals = onp.where(posinf_flips, onp.array(onp.inf, dtype=dtype), vals)
    vals = onp.where(neginf_flips, onp.array(-onp.inf, dtype=dtype), vals)
    vals = onp.where(nan_flips, onp.array(onp.nan, dtype=dtype), vals)

    return _cast_to_shape(onp.asarray(vals, dtype=dtype), shape, dtype)

  return rand

# TODO(mattjj): doesn't handle complex types
def rand_some_zero():
  """Return a random sampler that produces some zeros."""
  rng = npr.RandomState(1)
  base_rand = rand_default()

  def rand(shape, dtype):
    """The random sampler function."""
    dims = _dims_of_shape(shape)
    zeros = rng.rand(*dims) < 0.5

    vals = base_rand(shape, dtype)
    vals = onp.where(zeros, onp.array(0, dtype=dtype), vals)

    return _cast_to_shape(onp.asarray(vals, dtype=dtype), shape, dtype)

  return rand


def rand_int(low, high=None):
  randint = npr.RandomState(0).randint
  def fn(shape, dtype):
    return randint(low, high=high, size=shape, dtype=dtype)
  return fn

def rand_unique_int():
  randchoice = npr.RandomState(0).choice
  def fn(shape, dtype):
    return randchoice(onp.arange(onp.prod(shape), dtype=dtype),
                      size=shape, replace=False)
  return fn

def rand_bool():
  rng = npr.RandomState(0)
  def generator(shape, dtype):
    return _cast_to_shape(rng.rand(*_dims_of_shape(shape)) < 0.5, shape, dtype)
  return generator

def check_raises(thunk, err_type, msg):
  try:
    thunk()
    assert False
  except err_type as e:
    assert str(e).startswith(msg), "\n{}\n\n{}\n".format(e, msg)

def check_raises_regexp(thunk, err_type, pattern):
  try:
    thunk()
    assert False
  except err_type as e:
    assert re.match(pattern, str(e)), "{}\n\n{}\n".format(e, pattern)


def _iter_eqns(jaxpr):
  # TODO(necula): why doesn't this search in params?
  for eqn in jaxpr.eqns:
    yield eqn
  for subjaxpr in core.subjaxprs(jaxpr):
    yield from _iter_eqns(subjaxpr)

def assert_dot_precision(expected_precision, fun, *args):
  jaxpr = api.make_jaxpr(fun)(*args)
  precisions = [eqn.params['precision'] for eqn in _iter_eqns(jaxpr.jaxpr)
                if eqn.primitive == lax.dot_general_p]
  for precision in precisions:
    msg = "Unexpected precision: {} != {}".format(expected_precision, precision)
    assert precision == expected_precision, msg


_CACHED_INDICES: Dict[int, Sequence[int]] = {}

def cases_from_list(xs):
  xs = list(xs)
  n = len(xs)
  k = min(n, FLAGS.num_generated_cases)
  # Random sampling for every parameterized test is expensive. Do it once and
  # cache the result.
  indices = _CACHED_INDICES.get(n)
  if indices is None:
    rng = npr.RandomState(42)
    _CACHED_INDICES[n] = indices = rng.permutation(n)
  return [xs[i] for i in indices[:k]]

def cases_from_gens(*gens):
  sizes = [1, 3, 10]
  cases_per_size = int(FLAGS.num_generated_cases / len(sizes)) + 1
  for size in sizes:
    for i in range(cases_per_size):
      yield ('_{}_{}'.format(size, i),) + tuple(gen(size) for gen in gens)


class JaxTestCase(parameterized.TestCase):
  """Base class for JAX tests including numerical checks and boilerplate."""

  # TODO(mattjj): this obscures the error messages from failures, figure out how
  # to re-enable it
  # def tearDown(self) -> None:
  #   assert core.reset_trace_state()

  def assertArraysAllClose(self, x, y, check_dtypes, atol=None, rtol=None):
    """Assert that x and y are close (up to numerical tolerances)."""
    self.assertEqual(x.shape, y.shape)
    atol = max(tolerance(_dtype(x), atol), tolerance(_dtype(y), atol))
    rtol = max(tolerance(_dtype(x), rtol), tolerance(_dtype(y), rtol))

    _assert_numpy_allclose(x, y, atol=atol, rtol=rtol)

    if check_dtypes:
      self.assertDtypesMatch(x, y)

  def assertDtypesMatch(self, x, y):
    if FLAGS.jax_enable_x64:
      self.assertEqual(_dtype(x), _dtype(y))

  def assertAllClose(self, x, y, check_dtypes, atol=None, rtol=None):
    """Assert that x and y, either arrays or nested tuples/lists, are close."""
    if isinstance(x, dict):
      self.assertIsInstance(y, dict)
      self.assertEqual(set(x.keys()), set(y.keys()))
      for k in x.keys():
        self.assertAllClose(x[k], y[k], check_dtypes, atol=atol, rtol=rtol)
    elif is_sequence(x) and not hasattr(x, '__array__'):
      self.assertTrue(is_sequence(y) and not hasattr(y, '__array__'))
      self.assertEqual(len(x), len(y))
      for x_elt, y_elt in zip(x, y):
        self.assertAllClose(x_elt, y_elt, check_dtypes, atol=atol, rtol=rtol)
    elif hasattr(x, '__array__') or onp.isscalar(x):
      self.assertTrue(hasattr(y, '__array__') or onp.isscalar(y))
      if check_dtypes:
        self.assertDtypesMatch(x, y)
      x = onp.asarray(x)
      y = onp.asarray(y)
      self.assertArraysAllClose(x, y, check_dtypes=False, atol=atol, rtol=rtol)
    elif x == y:
      return
    else:
      raise TypeError((type(x), type(y)))

  def assertMultiLineStrippedEqual(self, expected, what):
    """Asserts two strings are equal, after stripping each line."""
    ignore_space_re = re.compile(r'\s*\n\s*')
    expected_clean = re.sub(ignore_space_re, '\n', expected.strip())
    what_clean = re.sub(ignore_space_re, '\n', what.strip())
    self.assertMultiLineEqual(expected_clean, what_clean,
                              msg="Found\n{}\nExpecting\n{}".format(what, expected))

  def _CompileAndCheck(self, fun, args_maker, check_dtypes,
                       rtol=None, atol=None):
    """Helper method for running JAX compilation and allclose assertions."""
    args = args_maker()

    def wrapped_fun(*args):
      self.assertTrue(python_should_be_executing)
      return fun(*args)

    python_should_be_executing = True
    python_ans = fun(*args)

    python_shapes = tree_map(lambda x: onp.shape(x), python_ans)
    onp_shapes = tree_map(lambda x: onp.shape(onp.asarray(x)), python_ans)
    self.assertEqual(python_shapes, onp_shapes)

    cache_misses = xla.xla_primitive_callable.cache_info().misses
    python_ans = fun(*args)
    self.assertEqual(
        cache_misses, xla.xla_primitive_callable.cache_info().misses,
        "Compilation detected during second call of {} in op-by-op "
        "mode.".format(fun))

    cfun = api.jit(wrapped_fun)
    python_should_be_executing = True
    monitored_ans = cfun(*args)

    python_should_be_executing = False
    compiled_ans = cfun(*args)

    self.assertAllClose(python_ans, monitored_ans, check_dtypes, atol, rtol)
    self.assertAllClose(python_ans, compiled_ans, check_dtypes, atol, rtol)

    args = args_maker()

    python_should_be_executing = True
    python_ans = fun(*args)

    python_should_be_executing = False
    compiled_ans = cfun(*args)

    self.assertAllClose(python_ans, compiled_ans, check_dtypes, atol, rtol)

  def _CheckAgainstNumpy(self, numpy_reference_op, lax_op, args_maker,
                         check_dtypes=False, tol=None):
    args = args_maker()
    lax_ans = lax_op(*args)
    numpy_ans = numpy_reference_op(*args)
    self.assertAllClose(numpy_ans, lax_ans, check_dtypes=check_dtypes,
                        atol=tol, rtol=tol)


@contextmanager
def ignore_warning(**kw):
  with warnings.catch_warnings():
    warnings.filterwarnings("ignore", **kw)
    yield
