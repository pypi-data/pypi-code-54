from abc import ABC, abstractmethod

import numpy as np


class Distribution(ABC):
    """Statistical distribution

    Used as a base for describing the distributions used to describe the possible values of the input variables.

    These Distribution's can also be converted to pymc3 Distributions if the pymc3
    optimiser is used.

    Parameters
    ----------

    Returns
    -------

    """
    name = "unknown"
    parameters = ()
    kwargs = {}

    def __init__(self, *args, **kwargs):
        self.kwargs = {}

        if len(args):
            for k, v in zip(self.parameters, args):
                kwargs[k[0]] = v
        for p in self.parameters:
            assert len(p) == 2

            if p[0] not in kwargs:
                self.kwargs[p[0]] = p[1]
            else:
                self.kwargs[p[0]] = kwargs[p[0]]

    def __repr__(self):
        options = ["{}={}".format(k, self.kwargs[k]) for k in self.kwargs]
        return "<{} {}>".format(self.name, ", ".join(options))

    def __getattr__(self, item):
        if item in self.kwargs:
            return self.kwargs[item]

    @abstractmethod
    def evaluate(self, n=1):
        return self.distribution.random(size=n)


class Scalar(Distribution):
    parameters = (
        ("value", 1.0),
    )

    def evaluate(self, n=1):
        return self.value * np.ones(n)


class Normal(Distribution):
    name = "Normal"

    parameters = (
        ("mu", 0.0),
        ("sigma", 1.0)
    )

    def evaluate(self, n=1):
        return np.random.normal(loc=self.mu, scale=self.sigma, size=n)


class Uniform(Distribution):
    name = "Uniform"

    parameters = (
        ("lower", 0.0),
        ("upper", 1.0)
    )

    def __init__(self, *args, **kwargs):
        super(Uniform, self).__init__(*args, **kwargs)

        if self.lower > self.upper:
            raise ValueError("upper must be greater than lower")

    def evaluate(self, n=1):
        return (self.upper - self.lower) * np.random.random(size=n) + self.lower


class Bound(Distribution):
    name = "Bound"

    parameters = [
        ("lower", 0.0),
        ("upper", 1.0)
    ]

    def __init__(self, distribution, **kwargs):
        super(Bound, self).__init__(**kwargs)
        if isinstance(distribution, Distribution):
            self.distribution = distribution
            self.distribution_cls = None
        else:
            self.distribution = None
            self.distribution_cls = distribution

    def __repr__(self):
        if self.distribution_cls:
            options = ["dist=" + self.distribution_cls.name]
            options = options + ["{}={}".format(k, self.kwargs[k]) for k in self.kwargs]
        else:
            options = ["dist=" + str(self.distribution)]
            options = options + ["{}={}".format(k, self.kwargs[k]) for k in self.kwargs]
        return "<{} {}>".format(self.name, ", ".join(options))

    def __call__(self, *args, **kwargs):
        return Bound(self.distribution_cls(**kwargs), **self.kwargs)

    def evaluate(self, n=1):
        f = self.distribution.evaluate(n)
        return np.clip(f, self.lower, self.upper)


class Function(Distribution):
    name = "Function"

    parameters = [
        ("function", None),
    ]

    def evaluate(self, n=1):
        f = self.kwargs["function"]
        return np.array([f() for i in range(n)])
