import math


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
    return a * pow(b, mod - 2, mod)


def ncr(n, r, mod=None):
    """
    scipy.misc.comb または scipy.special.comb と同じ
    組み合わせの数 nCr
    :param int n:
    :param int r:
    :param int mod: 3 以上の素数であること
    :rtype: int
    """
    assert n >= r

    def inv(a):
        """
        a の逆元
        :param a:
        :return:
        """
        return pow(a, mod - 2, mod)

    # 何度も呼ぶ場合は最大の n 以下の階乗を事前に計算しておくといい
    if mod:
        return math.factorial(n) * inv(math.factorial(r)) * inv(math.factorial(n - r)) % mod
    else:
        return math.factorial(n) // math.factorial(r) // math.factorial(n - r)


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
