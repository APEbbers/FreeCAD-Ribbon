from collections.abc import Mapping

# https://stackoverflow.com/questions/2082152/how-to-make-a-case-insensitive-dictionary/30221547#30221547
class CaseInsensitiveDict(dict):

    def __init__(self, data=None, **kwargs):
        self.update(data, **kwargs)

    def get(self, k, default=None):
        return super().get(k.lower(), default)

    def pop(self, k):
        return super().pop(k.lower())

    def setdefault(self, k, default=None):
        return super().setdefault(k.lower(), default)

    def update(self, data=None, **kwargs):
        if data is not None:
            if isinstance(data, Mapping):
                data = data.items()
            super().update((k.lower(), v) for k, v in data)
        super().update((k.lower(), v) for k, v in kwargs)

    def __contains__(self, k):
        return super().__contains__(k.lower())

    def __delitem__(self, k):
        super().__delitem__(k.lower())

    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return False
        if not isinstance(other, CaseInsensitiveDict):
            other = CaseInsensitiveDict(other)
        return super().__eq__(other)

    def __getitem__(self, k):
        return super().__getitem__(k.lower())

    def __setitem__(self, k, v):
        super().__setitem__(k.lower(), v)