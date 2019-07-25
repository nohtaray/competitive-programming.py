import math
from functools import reduce

from operator import mul


def get_divisors(n):
    """
    n の約数をリストで返す
    :param int n:
    :rtype: list of int
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
    :rtype: list of int
    """
    if n <= 1:
        return []

    ret = []
    while n > 2 and n % 2 == 0:
        ret.append(2)
        n //= 2
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            ret.append(i)
            n //= i
        else:
            i += 2
    ret.append(n)
    return ret


def div_mod(a, b, mod):
    """
    (a // b) % mod
    mod は 3 以上の素数を指定
    フェルマーの小定理より mod p の世界で b^(p-1) は必ず 1 になるので
    b の逆元 (b と掛けると 1 になる数) は b^(p-2)
    :param int a:
    :param int b:
    :param int mod:
    :return:
    """
    return a * pow(b, mod - 2, mod) % mod


def mod_inv(a, mod):
    """
    a の逆元
    :param int a:
    :param int mod:
    :return:
    """
    return pow(a, mod - 2, mod)


def ncr(n, r, mod=None):
    """
    scipy.misc.comb または scipy.special.comb と同じ
    組み合わせの数 nCr
    :param int n:
    :param int r:
    :param int mod: 3 以上の素数であること
    :rtype: int
    """
    if n < r:
        return 0

    # 何度も呼ぶ場合は combination.py をつかう
    r = min(n - r, r)
    if r == 0:
        return 1
    if mod:
        return reduce(mul, range(n, n - r, -1)) * mod_inv(reduce(mul, range(r, 0, -1)), mod) % mod
    else:
        # math.factorial よりこっちのが速い
        # https://atcoder.jp/contests/abc110/submissions?f.Task=&f.Language=&f.Status=&f.User=nohtaray
        return reduce(mul, range(n, n - r, -1)) // reduce(mul, range(r, 0, -1))


def nhr(n, r, mod=None):
    """
    重複組み合わせの総数 nHr
    :param int n:
    :param int r:
    :param int mod:
    :return:
    """
    return ncr(n + r - 1, r, mod)


def get_primes(max=None, count=None):
    """
    素数列挙
    昇順にソートされています
    https://qiita.com/Ishotihadus/items/73e107271275611f05f2
    :param int max:
    :param int count:
    :return:
    """
    assert max or count
    if count:
        raise NotImplementedError()
    if max <= 1:
        return []

    primes = [2]
    sieve = [False for _ in range(max + 1)]
    p = 3
    while p <= max:
        primes.append(p)
        sieve[p] = True
        if p <= math.sqrt(max):
            for i in range(p * (p | 1), max + 1, p * 2):
                sieve[i] = True
        while p <= max and sieve[p]:
            p += 2

    return primes
