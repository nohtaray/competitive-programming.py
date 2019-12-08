def ModInt(mod):
    class _ModInt:
        def __init__(self, value):
            self.value = value % mod

        def __add__(self, other):
            if isinstance(other, _ModInt):
                return _ModInt(self.value + other.value)
            else:
                return _ModInt(self.value + other)

        def __sub__(self, other):
            if isinstance(other, _ModInt):
                return _ModInt(self.value - other.value)
            else:
                return _ModInt(self.value - other)

        def __radd__(self, other):
            return self.__add__(other)

        def __mul__(self, other):
            if isinstance(other, _ModInt):
                return _ModInt(self.value * other.value)
            else:
                return _ModInt(self.value * other)

        def __truediv__(self, other):
            raise NotImplementedError()

        def __int__(self):
            return self.value

        def __repr__(self):
            return str(self.value)

    return _ModInt


if __name__ == '__main__':
    MI7 = ModInt(mod=7)
    assert int(MI7(1) + MI7(8)) == 2
    assert int(MI7(1) + 8) == 2
    assert int(8 + MI7(1)) == 2
