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


def get_montmort_numbers(max, mod):
    """
    0 ... max までのモンモール数
    整数 1, 2, 3, …, n を要素とする順列において、i 番目 (i ≤ n) が i でない順列 (完全順列, 攪乱順列) の個数。
    1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496, ...
    https://ja.wikipedia.org/wiki/完全順列
    https://oeis.org/A000166
    :param int max:
    :param int mod:
    """
    dp = [0] * (max + 1)
    dp[0] = 1
    dp[1] = 0
    for i in range(2, len(dp)):
        dp[i] = (dp[i - 1] + dp[i - 2]) * (i - 1) % mod
    return dp[:max + 1]
