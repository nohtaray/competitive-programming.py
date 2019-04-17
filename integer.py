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


def get_factors(n):
    """
    素因数分解
    :param int n:
    :type: list of int
    """
    ret = []
    i = 2
    while 2 <= i <= n:
        if n % i == 0:
            ret.append(i)
            n //= i
        else:
            i += 1
    return ret
