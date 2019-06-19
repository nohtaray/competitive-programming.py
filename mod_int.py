class ModInt:
    def __init__(self, value, mod):
        self.value = value % mod
        self._mod = mod

    def __add__(self, other):
        if isinstance(other, ModInt):
            return ModInt(self.value + other.value, self._mod)
        else:
            return ModInt(self.value + other, self._mod)

    def __mul__(self, other):
        if isinstance(other, ModInt):
            return ModInt(self.value * other.value, self._mod)
        else:
            return ModInt(self.value * other, self._mod)

    def __truediv__(self, other):
        # TODO: 実装
        raise NotImplementedError()

    def __repr__(self):
        return str(self.value)
