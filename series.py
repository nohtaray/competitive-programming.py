import itertools


def triangle(n):
    """
    n 番目の三角数
    https://ja.wikipedia.org/wiki/三角数
    1, 3, 6, 10, 15, 21, ...
    1 から n までの累積和
    :param int n:
    :return:
    """
    assert n >= 1
    return n * (n + 1) // 2


def triangular_pyramid(n):
    """
    n 番目の三角錐数
    https://ja.wikipedia.org/wiki/三角錐数
    1, 4, 10, 20, 35, 56, ...
    1 番目から n 番目の三角数の累積和
    :param int n:
    :return:
    """
    assert n >= 1
    return n * (n + 1) * (n + 2) // 6


def factorials(max, mod=None):
    """
    階乗 0!, 1!, 2!, ..., max!
    :param int max:
    :param int mod:
    :return:
    """
    ret = [1]
    n = 1
    if mod:
        for i in range(1, max + 1):
            n *= i
            n %= mod
            ret.append(n)
    else:
        for i in range(1, max + 1):
            n *= i
            ret.append(n)
    return ret


# https://atcoder.jp/contests/abc066/submissions/5721975
def mod_invs(max, mod):
    """
    逆元のリスト 0 から max まで
    https://atcoder.jp/contests/abc127/submissions/5630531
    ここから。あんまり良くわかってない
    :param max:
    :param mod:
    :return:
    """
    invs = [1] * (max + 1)
    for x in range(2, max + 1):
        invs[x] = (-(mod // x) * invs[mod % x]) % mod
    return invs


def get_ncrs(n, mod):
    """
    nC_0, nC_1, nC_2, ..., nC_n までのリスト
    :param n:
    :param mod:
    :return:
    """
    invs = mod_invs(n, mod)
    ret = [1]
    ncr = 1
    for i in range(1, n + 1):
        ncr = ((ncr * (n - i + 1) % mod) * invs[i]) % mod
        ret.append(ncr)
    return ret


def get_powers(x, n, mod=None):
    """
    x の累積積 [x^0, x^1, x^2, ..., x^(n-1)]
    :param x:
    :param int n:
    :param int mod:
    """
    if n <= 0:
        return []

    if mod is not None:
        return list(itertools.accumulate([1] * n, lambda p, _: p * x % mod))
    else:
        return list(itertools.accumulate([1] * n, lambda p, _: p * x))
