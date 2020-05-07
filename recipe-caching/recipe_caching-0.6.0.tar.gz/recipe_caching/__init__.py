# -*- coding: utf-8 -*-
"""
Recipe
~~~~~~~~~~~~~~~~~~~~~
"""
import functools

from recipe_caching.caching_query import CachingQuery


def query_callable(regions, query_cls=CachingQuery, **kwargs):
    return functools.partial(query_cls, regions, **kwargs)


__all__ = [query_callable]
