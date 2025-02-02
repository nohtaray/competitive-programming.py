import math
from functools import reduce
from operator import mul

from atcoder._math import _is_prime, _primitive_root


def is_prime(n):
    """
    素数判定
    from atcoder._math import _is_prime, _primitive_root
    """
    return _is_prime(n)


def primitive_root(p):
    """
    p の原始根
    from atcoder._math import _is_prime, _primitive_root
    """
    return _primitive_root(p)


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
    b と mod は互いに素であること
    :param int a:
    :param int b:
    :param int mod:
    """
    return a * mod_inv(b, mod) % mod


def mod_inv(a, mod):
    """
    a の逆元
    mod は a と互いに素であること
    :param a:
    :param mod:
    :return:
    """
    b = mod
    u = 1
    v = 0
    while b:
        t = a // b
        a -= t * b
        a, b = b, a
        u -= t * v
        u, v = v, u
    u %= mod
    return u


def ncr(n, r, mod=None):
    """
    組み合わせの数 nCr
    :param int n:
    :param int r:
    :param int mod: 3 以上の素数であること
    :rtype: int
    """
    if n < r:
        return 0

    # n が 10**6 * 2 のときに TLE した
    # https://atcoder.jp/contests/agc051/submissions/60117826
    # 覚えたら関数ごと消す
    raise "遅いので combination.py を使ってください"

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
    """
    return ncr(n + r - 1, r, mod)


def get_primes(max=None, count=None):
    """
    素数列挙
    昇順にソートされています
    https://qiita.com/Ishotihadus/items/73e107271275611f05f2
    :param int max:
    :param int count:
    """
    assert max is not None or count is not None
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


def pow_pow(a, b, c, mod):
    """
    (a^(b^c)) % mod
    mod は素数
    """
    if a % mod == 0:
        return 0
    return pow(a, pow(b, c, mod - 1), mod)


def extgcd(a, b):
    """
    extgcd(a, b): ax + by = gcd(a, b) となる整数 x, y を返す
    https://qiita.com/drken/items/b97ff231e43bce50199a#3-4-拡張ユークリッドの互除法のアルゴリズム的記述
    負の値を渡しても OK
    verify: https://atcoder.jp/contests/abc340/submissions/59184365
    :param int a:
    :param int b:
    :return: (gcd(a, b), x, y)
    """
    if b == 0:
        return a, 1, 0
    # a = qb + r
    q = a // b
    r = a % b
    d, x, y = extgcd(b, r)
    return d, y, x - q * y


def find_integer_solutions(a, b, c, k=0):
    """
    不定方程式 ax + by = c の整数解を求める
    :param int a:
    :param int b:
    :param int c:
    :param int k:
    :rtype: None|(int,int)
    """
    # 最大公約数を求める
    g = math.gcd(a, b)

    # c が gcd(a, b) で割り切れない場合、解は存在しない
    if c % g != 0:
        return None

    # a と b を gcd で割り、簡約化
    a, b, c = a // g, b // g, c // g
    _, x0, y0 = extgcd(a, b)
    x0 *= c
    y0 *= c

    # k はなんでもいい
    x = x0 + k * b
    y = y0 - k * a
    return x, y


def mod_log(x, base, mod, allow_zero=True):
    """
    log_{base}(x) % mod
    x == {base}^{ret} % mod
    https://qiita.com/drken/items/3b4fdf0a78e7a138cd9a#6-離散対数-log_a-x
    BSGS; baby-step giant-step
    https://atcoder.jp/contests/arc042/submissions/14086715
    :param x:
    :param base:
    :param mod:
    :param bool allow_zero:
    """
    if not 0 < x < mod:
        return None
    if allow_zero and x == 1:
        return 0
    base %= mod
    sqrt_mod = int(math.sqrt(mod)) + 1
    # ret = p * sqrt(mod) + r
    # a_r[z]: base^r == z となる最小の r
    a_r = {}
    z = 1
    for r in range(sqrt_mod):
        if z not in a_r:
            a_r[z] = r
        z *= base
        z %= mod

    # A == (1 / base^{sqrt(mod)})
    A = mod_inv(pow(base, sqrt_mod, mod), mod)
    z = x
    for p in range(sqrt_mod):
        if z in a_r:
            r = a_r[z]
            if not r == p == 0:
                break
        z *= A
        z %= mod
    else:
        return None
    return p * sqrt_mod + r
