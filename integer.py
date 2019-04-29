import math
from functools import reduce
from operator import mul


def get_divisors(n):
    """
    n の約数をリストで返す
    :param int n:
    :rtype: list of int
    """
    ret = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            ret.append(i)
            if n // i != i:
                ret.append(n // i)
    return ret


def get_factors(n):
    """
    素因数分解
    :param int n:
    :rtype: list of int
    """
    if n <= 1:
        return []

    ret = []
    while n > 2 and n % 2 == 0:
        ret.append(2)
        n //= 2
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            ret.append(i)
            n //= i
        else:
            i += 2
    ret.append(n)
    return ret


def comb(n, r):
    """
    scipy.misc.comb または scipy.special.comb と同じ
    組み合わせの数 nCr
    :param int n:
    :param int r:
    :rtype: int
    """
    assert n >= r
    r = min(n - r, r)
    if r == 0:
        return 1
    return reduce(mul, range(n, n - r, -1)) // reduce(mul, range(r, 0, -1))


def comb_rep(n, r):
    """
    重複組み合わせの総数 nHr
    :param int n:
    :param int r:
    :return:
    """
    return comb(n + r - 1, r)
