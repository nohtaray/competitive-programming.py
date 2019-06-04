import itertools
import operator


def cummax(it):
    """
    np.maximum.accumulate(arr) でもよさそう
    https://stackoverflow.com/questions/33569668/numpy-max-vs-amax-vs-maximum

    累積 max
    :param collections.Iterable it:
    :return:
    """
    return list(itertools.accumulate(it, max))


def cummin(it):
    """
    累積 min
    :param collections.Iterable it:
    :return:
    """
    return list(itertools.accumulate(it, min))


def cumsum(it):
    """
    累積和
    :param collections.Iterable it:
    :return:
    """
    return list(itertools.accumulate(it, operator.add))


if __name__ == "__main__":
    li = [3, 1, 4, 1, 5, 9, 2, 6]
    assert cummax(li) == [3, 3, 4, 4, 5, 9, 9, 9]
    assert cummin(li) == [3, 1, 1, 1, 1, 1, 1, 1]
    assert cumsum(li) == [3, 4, 8, 9, 14, 23, 25, 31]
