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


def get_factorials(max, mod=None):
    import libs.combination
    return libs.combination.get_factorials(max=max, mod=mod)


def mod_invs(max, mod):
    import libs.combination
    return libs.combination.mod_invs(max=max, mod=mod)


def factorial_invs(max, mod):
    import libs.combination
    return libs.combination.factorial_invs(max=max, mod=mod)


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
