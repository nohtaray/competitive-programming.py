import math
from functools import reduce
from operator import mul


def get_divisors(n):
    """
    n の約数をリストで返す
    :param int n:
    :return:
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
    :type: list of int
    """
    ret = []
    i = 2
    while 2 <= i <= n:
        if n % i == 0:
            ret.append(i)
            n //= i
        else:
            i += 1
    return ret


def comb(n, r):
    """
    scipy.misc.comb または scipy.special.comb と同じ
    組み合わせの数 nCr
    :param int n:
    :param int r:
    :rtype: int
    """
    r = min(n - r, r)
    if r == 0:
        return 1
    return reduce(mul, range(n, n - r, -1)) // reduce(mul, range(r, 0, -1))
