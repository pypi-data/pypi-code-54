import truelayer.auth
from datetime import datetime, time, date, timedelta

from marshmallow import fields


class WithIdentityMixin:
    identity_type = None

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, self.identity_type):
            return value
        return super()._deserialize(value, attr, data, **kwargs)


class DateTime(WithIdentityMixin, fields.DateTime):
    identity_type = datetime


class Date(WithIdentityMixin, fields.Date):
    identity_type = date


def Nested(cls):
    class InnerNested(WithIdentityMixin, fields.Nested):
        _identity_type = cls

        @property
        def identity_type(self):
            import truelayer.auth.models
            if isinstance(self._identity_type, str):
                self._identity_type = getattr(truelayer.auth.models, self._identity_type)
            return self._identity_type
    return InnerNested


__all__ = [
    'Nested',
    'DateTime',
    'Date'
]