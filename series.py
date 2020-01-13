import itertools


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
