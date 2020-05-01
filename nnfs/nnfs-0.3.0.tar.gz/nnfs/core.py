import numpy as np
import inspect


# Initializes NNFS
def init(dot_precision_woraround=True, default_dtype='float32', random_seed=0):

    # Numpy methods to be replaced for a workaround
    methods_to_enclose = [
        [np, 'zeros', False],
        [np.random, 'randn', True],
    ]

    # https://github.com/numpy/numpy/issues/15591
    # np.dot() is not consistent between machines
    # This workaround raises consistency
    # we make computations using float64, but return float32 data
    if dot_precision_woraround:
        orig_dot = np.dot
        def dot(*args, **kwargs):
            return orig_dot(*[a.astype('float64') for a in args], **kwargs).astype('float32')
        np.dot = dot
    else:
        methods_to_enclose.append([np, 'dot', False])

    # https://github.com/numpy/numpy/issues/6860
    # It is not possible to set default datatype with numpy
    # To make it able to enable and disable above workaround and set dtype
    # we'll enclose numpy method's with own one which will force different datatype
    if default_dtype:
        for method in methods_to_enclose:
            enclose(method, default_dtype)

    # Set seed to the given value (0 by default)
    if random_seed is not None:
        np.random.seed(random_seed)


# Encloses numpy method
def enclose(method, default_dtype):

    # Save a handler to original method
    method.append(getattr(*method))
    def enclosed_method(*args, **kwargs):

        # If flag is True - use .astype()
        if method[2]:
            return method[3](*args, **kwargs).astype(default_dtype)

        # Else pass dtype in kwargs
        else:
            if 'dtype' not in kwargs:
                kwargs['dtype'] = default_dtype
            return method[3](*args, **kwargs)

    # Replace numpy method with enclosed one
    setattr(*method[:2], enclosed_method)
