def cummax(it, first=-float('inf')):
    """
    np.maximum.accumulate(arr) でもよさそう
    https://stackoverflow.com/questions/33569668/numpy-max-vs-amax-vs-maximum

    累積 max
    :param collections.Iterable it:
    :param float first:
    :return:
    """
    cm = first
    ret = []
    for v in it:
        cm = max(v, cm)
        ret.append(cm)
    return ret


def cummin(it, first=float('inf')):
    """
    累積 min
    :param collections.Iterable it:
    :param float first:
    :return:
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
    :return:
    """
    cs = 0
    ret = []
    for v in it:
        cs += v
        ret.append(cs)
    return ret


def argsort(li, key=None, reverse=False):
    return [i for _, i in sorted(
        [(a, i) for i, a in enumerate(li)], key=(lambda t: key(t[0])) if key else None, reverse=reverse
    )]


if __name__ == "__main__":
    li = [3, 1, 4, 1, 5, 9, 2, 6]
    assert cummax(li) == [3, 3, 4, 4, 5, 9, 9, 9]
    assert cummin(li) == [3, 1, 1, 1, 1, 1, 1, 1]
    assert cumsum(li) == [3, 4, 8, 9, 14, 23, 25, 31]
