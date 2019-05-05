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
