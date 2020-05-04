#  Copyright (c) 2020 Maksim Penkov
#  SPDX-License-Identifier: Apache-2.0

import inspect


class TupleDestructuringFactory:
    def __init__(self, lookup_root):
        assert _is_named_tuple(lookup_root)
        self._lookup_root = lookup_root

    def __call__(self, factory, whatever):
        if not _is_named_tuple(whatever):
            return None

        path = _resolve_namedtuple_path(self._lookup_root, whatever)

        if not path:
            return None

        root_instance = factory.obtain(self._lookup_root)

        if inspect.isawaitable(root_instance):
            return _destructure_async(root_instance, path)

        return _destructure(root_instance, path)


def _resolve_namedtuple_path(root, target, path=None):
    path = path or []

    for key, annotation in root.__annotations__.items():
        if not _is_named_tuple(annotation):
            continue

        new_path = [*path, key]
        if annotation is target:
            return new_path

        sub_path = _resolve_namedtuple_path(annotation, target, new_path)
        if sub_path:
            return sub_path

    return None


def _destructure(instance, path):
    while path:
        step = path.pop(0)
        instance = getattr(instance, step)
    return instance


async def _destructure_async(async_instance, path):
    return _destructure(
        await async_instance,
        path
    )


def _is_named_tuple(whatever):
    return hasattr(whatever, '_fields') and hasattr(whatever, '__annotations__')
