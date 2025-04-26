import math

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


def get_orders(A, prime):
    """
    A の各要素の位数を求める
    :param list of int A:
    :param int prime:
    :rtype: list of int
    """
    N = len(A)
    factors = list(set(get_factors(prime - 1)))
    ret = [0] * N
    for i in range(N):
        # https://atcoder.jp/contests/abc335/editorial/9042
        x = prime - 1
        for f in factors:
            while x % f == 0:
                x //= f
            t = pow(A[i], x, prime)
            while t != 1:
                t = pow(t, f, prime)
                x *= f
        ret[i] = x
    return ret


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


def find_integer_solutions(a, b, c, positive_only=False, k=None):
    """
    不定方程式 ax + by = c の整数解を求める
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

    if k is None:
        # y が最も小さい 0 以上の整数になる k を適当に設定
        k = y0 // a
        # # x が最も小さい 0 以上の整数になる k を適当に設定
        # k = (-x0 + b - 1) // b
    if positive_only:
        # (x := x0 + k * b) < 0
        # (y := y0 - k * a) < 0
        # not (-x0 / b <= k <= y0 / a)
        if -x0 > k * b or k * a > y0:
            return None
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
