import math


def trisect_real(fn, lo, hi, iter=150):
    """
    fn の結果が最も小さくなる引数を三分探索する
    :param callable fn:
    :param int lo: 最小のインデックス
    :param int hi: 最大のインデックス
    :param int iter: ループ回数
    :return: (value, x) lo <= x <= hi
    """
    if lo >= hi:
        return fn(lo), lo

    D = 2 / (1 + math.sqrt(5))
    l = lo
    r = hi
    m2 = lo + (hi - lo) * D
    m1 = lo + (m2 - lo) * D

    v1 = fn(m1)
    v2 = fn(m2)
    for _ in range(iter):
        if not (l < m1 < m2 < r):
            break
        if v1 < v2:
            m1, m2, r = l + (m2 - m1), m1, m2
            v2 = v1
            v1 = fn(m1)
        else:
            l, m1, m2 = m1, m2, r - (m2 - m1)
            v1 = v2
            v2 = fn(m2)
    return (v1, m1) if v1 < v2 else (v2, m2)


def trisect_real_maximize(fn, lo, hi, iter=150):
    """
    fn の結果が最も大きくなる引数を三分探索する
    :param callable fn:
    :param int lo: 最小のインデックス
    :param int hi: 最大のインデックス
    :param int iter: ループ回数
    :return: (value, x) lo <= x <= hi
    """
    (val, i) = trisect_real(lambda x: -fn(x), lo, hi, iter)
    return -val, i


def trisect_int(fn, lo, hi):
    """
    fn の結果が最も小さくなるインデックスを三分探索する
    :param callable fn:
    :param int lo: 最小のインデックス
    :param int hi: 最大のインデックス
    :return: (value, i) lo <= i <= hi
    """
    if lo >= hi:
        return fn(lo), lo

    INF = float("inf")
    fib = [1, 1, 2]
    while fib[-1] < hi - lo + 2:
        fib.append(fib[-1] + fib[-2])
    l = lo - 1
    m1 = l + fib[-3]
    m2 = l + fib[-2]
    r = l + fib[-1]

    v1 = fn(m1)
    v2 = fn(m2)
    while r - l > 3:
        if v1 < v2:
            m1, m2, r = l + (m2 - m1), m1, m2
            v2 = v1
            v1 = fn(m1) if lo <= m1 <= hi else INF
        else:
            l, m1, m2 = m1, m2, r - (m2 - m1)
            v1 = v2
            v2 = fn(m2) if lo <= m2 <= hi else INF
    return (v1, m1) if v1 < v2 else (v2, m2)


def trisect_int_maximize(fn, lo, hi):
    """
    fn の結果が最も大きくなるインデックスを三分探索する
    :param callable fn:
    :param int lo: 最小のインデックス
    :param int hi: 最大のインデックス
    :return: (value, i) lo <= i <= hi
    """
    (val, i) = trisect_int(lambda x: -fn(x), lo, hi)
    return -val, i
