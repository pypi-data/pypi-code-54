from collections.abc import Mapping, Sequence

class ValidationError(Exception):
    def __init__(self, msg, path):
        path_str = ".".join(str(x) for x in path)
        super().__init__(f"{msg} @ {path_str}")
        self.path = path

class Context:
    def __init__(self, path = ["$"]):
        self.path = path
    def descend(self, path_chunk):
        return Context(self.path + [path_chunk])
    def error(self, msg):
        raise ValidationError(msg, self.path)

class ExplorerList(Sequence):
    def __init__(self, value, ctx):
        self.value = value
        self.ctx  = ctx
    def __getitem__(self, ix):
        if ix >= self.value.__len__():
            self.ctx.error(f"Expecting list to have element at position: {ix}.")
        return Explorer(self.value[ix], self.ctx.descend(ix))
    def __len__(self):
        return self.value.__len__()

class ExplorerObject(Mapping):
    def __init__(self, value, ctx):
        self.value = value
        self.ctx = ctx
    def __getitem__(self, key):
        if key not in self.value:
            self.ctx.error(f"Expecting object to have key: {key}.")
        return Explorer(self.value[key], self.ctx.descend(key))
    def __iter__(self):
        return self.value.__iter__()
    def __len__(self):
        return self.value.__len__()

class Explorer:
    def __init__(self, value, ctx = Context()):
        self.value = value
        self.ctx = ctx
    def validate(self, validator):
        msg = validator.validate(self.value)
        if msg is not None:
            raise ValidationError(msg, self.path)
    def as_dict(self):
        if not isinstance(self.value,dict):
            self.ctx.error("Expecting object.")
        return ExplorerObject(self.value, self.ctx)
    def as_list(self):
        if not isinstance(self.value,list):
            self.ctx.error("Expecting list.")
        return ExplorerList(self.value, self.ctx)