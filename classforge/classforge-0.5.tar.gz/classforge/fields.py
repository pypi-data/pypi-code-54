# (C) Michael DeHaan <michaeldehaan.net>, 2020



class Field(object):

    __slots__ = [
        'name',
        'type',
        'default',
        'nullable',
        'mutable',
        'accessor',
        'mutator',
        '_mutated',
        'choices',
        'value',
        'required',
        'remap',
        'hidden',
        'encode',
        'decode'
    ]

    def __init__(self, name=None, type=None, default=None, nullable=True, mutable=True, mutator=None, accessor=None,
                 choices=None, required=False, hidden=False, remap=None, encode=None, decode=None):

        assert mutator is None or (isinstance(mutator, str))
        assert accessor is None or (isinstance(accessor, str))

        self.type = type
        self.default = default
        self.nullable = nullable
        self.mutable = mutable
        self.mutator = mutator
        self._mutated = False
        self.accessor = accessor
        self.choices = choices
        self.value = None
        self.required = required
        self.hidden = hidden
        self.remap = remap
        self.encode = encode
        self.decode = decode

        if default is not None and self.value is None:
            self.value = default

    def _show(self):

        # this is just used for debugging, not part of a public API
        return dict(
            type = self.type,
            default = self.default,
            nullable = self.nullable,
            mutable = self.mutable,
            mutator = self.mutator,
            accessor = self.accessor,
            choices = self.choices,
            value = self.value,
            required = self.required,
            remap = self.remap,
            hidden = self.hidden,
            encode = self.encode,
            decode = self.decode
        )

    def copy(self):
        obj = self.__class__(type=self.type, default=self.default, nullable=self.nullable, mutable=self.mutable,
                    mutator=self.mutator, accessor=self.accessor, choices=self.choices, required=self.required,
                    remap=self.remap, hidden=self.hidden, encode=self.encode, decode=self.decode)
        obj._mutated = False
        obj.value = self.value
        return obj

    def _INTERNAL_get(self, parent, name):
        # return the value of the field
        return self._find_function(parent, self.accessor, self.field_access, "get_%s" % name)(self.value)

    def _INTERNAL_serialize(self, parent, name, value, remap_name):
        return self._find_function(parent, self.encode, self.field_encode, "encode_%s" % name)(value, remap_name)

    def _INTERNAL_deserialize(self, parent, name, value, remap_name):
        return self._find_function(parent, self.decode, self.field_decode, "decode_%s" % name)(value, remap_name)

    def _INTERNAL_set(self, parent, name, value):
        # set the value of the field
        self._mutated = True

        if not self.mutable and self._mutated:
            raise ValueError("field is immutable: %s" % name)

        if value is None and not self.nullable:
            raise ValueError("field is not nullable: %s" % name)

        if (self.nullable and value is not None) and (self.type is not None) and not isinstance(value, self.type):
            raise ValueError("invalid field type for %s. got %s, expected: %s" % (name, value, self.type))

        if self.choices is not None and not value in self.choices:
            raise ValueError("rejected value for %s: choices=%s" % (name, self.choices))

        fn = self._find_function(parent, self.mutator, self.field_mutate, "set_%s" % name)
        self.value = fn(value)

    def _find_function(self, parent, member, default_func, func_pattern):
        if member is None:
            # no named mutator function was passed into the field, so...
            fn2 = getattr(parent, func_pattern, None)
            if fn2 is not None:
                # use a funciton named get/set_<fieldname> if available...
                return fn2
        else:
            # a named member function was specified, so use if available, or error
            fn3 = getattr(parent, member, None)
            if fn3 is None:
                raise AttributeError("missing function: %s" % member)
            return fn3
        return default_func

# =======
# methods below this line are safe to subclass:

    def field_access(self, value):
        # optionally could override this in a subclass
        return value

    def field_mutate(self, value):
        # optionally could override this in a subclass
        return value

    def field_encode(self, value, remap_name):
        if hasattr(value, 'to_dict'):
            return value.to_dict()
        return value

    def field_decode(self, value, remap_name):
        if hasattr(self.type, 'from_dict'):
            return self.type.from_dict(value)
        else:
            return value
