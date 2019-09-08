def bright(fn, x, lo, hi):
    """
    lo から hi-1 のうち、fn の結果が x 以下となる、最も右の値 + 1
    bisect.bisect_right と同じ
    https://docs.python.org/ja/3/library/bisect.html
    :param callable fn:
    :param x:
    :param int lo: 最小値
    :param int hi: 最大値 + 1
    :return: lo <= ret <= hi
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if x < fn(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def bleft(fn, x, lo, hi):
    """
    (memo) いっぱい呼ぶなら np.searchsorted のほうがベクトル化されててはやそう
    lo から hi-1 のうち、fn の結果が x 以上となる、最も左の値
    bisect.bisect_left と同じ
    https://docs.python.org/ja/3/library/bisect.html
    :param callable fn:
    :param x:
    :param int lo: 最小値
    :param int hi: 最大値 + 1
    :return: lo <= ret <= hi
    """
    while lo < hi:
        mid = (lo + hi) // 2
        if fn(mid) < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
