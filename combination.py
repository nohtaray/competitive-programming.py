from libs.series import get_factorials, factorial_invs


class Combination:
    def __init__(self, max, mod):
        """
        :param int max:
        :param int mod: 3 以上の素数であること
        """
        self._factorials = get_factorials(max, mod)
        self._finvs = factorial_invs(max, mod)
        self._mod = mod

    def ncr(self, n, r):
        """
        :param int n:
        :param int r:
        :rtype: int
        """
        if n < r:
            return 0
        return self._factorials[n] * self._finvs[r] % self._mod * self._finvs[n - r] % self._mod


if __name__ == '__main__':
    assert Combination(5, 10 ** 9 + 7).ncr(5, 3) == 10
    assert Combination(5, 10 ** 9 + 7).ncr(5, 1) == 5
    assert Combination(5, 7).ncr(5, 3) == 3
