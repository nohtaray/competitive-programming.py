import math


def get_divisors(n):
    """
    n の約数をリストで返す
    :param int n:
    :return:
    """
    ret = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            ret.append(i)
            if n // i != i:
                ret.append(n // i)
    return ret
