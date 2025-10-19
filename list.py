from collections import Counter, defaultdict

import itertools

from libs.integer import get_factors


def cummax(it, first=-float("inf")):
    """
    累積 max
    :param collections.Iterable it:
    :param float first:
    """
    cm = first
    ret = []
    for v in it:
        cm = max(v, cm)
        ret.append(cm)
    return ret


def cummin(it, first=float("inf")):
    """
    累積 min
    :param collections.Iterable it:
    :param float first:
    """
    cm = first
    ret = []
    for v in it:
        cm = min(v, cm)
        ret.append(cm)
    return ret


def cumsum(it):
    """
    累積和
    :param collections.Iterable it:
    """
    cs = 0
    ret = []
    for v in it:
        cs += v
        ret.append(cs)
    return ret


def cumsum2(arr):
    H = len(arr)
    W = len(arr[0])
    ret = [[0] * (W + 1) for _ in range(H + 1)]
    for h, w in itertools.product(range(H), range(W)):
        ret[h + 1][w + 1] = ret[h][w + 1] + ret[h + 1][w] - ret[h][w] + arr[h][w]
    return ret


def cumsum3(arr):
    """
    3次元累積和
    cum[rx][ry][rz] - cum[lx][ry][rz] - cum[rx][ly][rz] - cum[rx][ry][lz] + cum[lx][ly][rz] + cum[lx][ry][lz] + cum[rx][ly][lz] - cum[lx][ly][lz]
    """
    X = len(arr)
    Y = len(arr[0])
    Z = len(arr[0][0])
    ret = [[[0] * (X + 1) for _ in range(Y + 1)] for _ in range(Z + 1)]
    for x, y, z in itertools.product(range(X), range(Y), range(Z)):
        ret[x + 1][y + 1][z + 1] = (
            ret[x][y + 1][z + 1]
            + ret[x + 1][y][z + 1]
            + ret[x + 1][y + 1][z]
            - ret[x][y][z + 1]
            - ret[x][y + 1][z]
            - ret[x + 1][y][z]
            + ret[x][y][z]
            + arr[x][y][z]
        )
    return ret


def cummax2(arr):
    H = len(arr)
    W = len(arr[0])
    ret = [[-float("inf")] * (W + 1) for _ in range(H + 1)]
    for h, w in itertools.product(range(H), range(W)):
        ret[h + 1][w + 1] = max(ret[h][w + 1], ret[h + 1][w], arr[h][w])
    return ret


def lcm(it, mod):
    """
    :param collections.Iterable it:
    :param int|None mod:
    :rtype: int
    """
    factors = defaultdict(int)
    for a in it:
        for f, cnt in Counter(get_factors(a)):
            factors[f] = max(factors[f], cnt)
    ret = 1
    if mod:
        for f, cnt in factors.items():
            ret *= pow(f, cnt, mod)
            ret %= mod
    else:
        for f, cnt in factors.items():
            ret *= pow(f, cnt)
    return ret


def argsort(li, key=None, reverse=False):
    return [
        i
        for _, i in sorted(
            [(a, i) for i, a in enumerate(li)],
            key=(lambda t: key(t[0])) if key else None,
            reverse=reverse,
        )
    ]


if __name__ == "__main__":
    li = [3, 1, 4, 1, 5, 9, 2, 6]
    assert cummax(li) == [3, 3, 4, 4, 5, 9, 9, 9]
    assert cummin(li) == [3, 1, 1, 1, 1, 1, 1, 1]
    assert cumsum(li) == [3, 4, 8, 9, 14, 23, 25, 31]
    assert argsort([3, 1, 2]) == [1, 2, 0]
