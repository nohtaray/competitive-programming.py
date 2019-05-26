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
