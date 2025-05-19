import math


def hilbert_order(x, y, pow, rotate=0):
    """
    https://codeforces.com/blog/entry/61203
    これ使わずに普通にソートしたのを C++ に変換して投げたほうがはやそげ
    https://atcoder.jp/contests/abc242/submissions/me
    :param x:
    :param y:
    :param pow: 最大の x, y が 2^pow 未満であること
    :param rotate:
    :return:
    """
    if pow == 0:
        return 0
    hpow = 1 << (pow - 1)
    if x < hpow:
        if y < hpow:
            seg = 0
        else:
            seg = 3
    else:
        if y < hpow:
            seg = 1
        else:
            seg = 2

    seg = (seg + rotate) & 3
    nx = x & (hpow - 1)
    ny = y & (hpow - 1)
    nrot = (rotate + (3 if seg == 0 else 0 if seg == 1 or seg == 2 else 1)) & 3
    sub_square_size = 1 << (2 * (pow - 1))
    ans = seg * sub_square_size
    add = hilbert_order(nx, ny, pow - 1, nrot)
    ans += add if seg == 1 or seg == 2 else (sub_square_size - add - 1)

    return ans


if __name__ == "__main__":
    N = 10**5
    QUERIES = []
    # mo's algorithm
    sqr = math.sqrt(N)
    LRI = [(l, r + 1, i) for i, (l, r) in enumerate(QUERIES)]
    LRI.sort(key=lambda x: (x[0] // sqr, x[1] if x[0] // sqr % 2 == 0 else -x[1]))
    # p = math.ceil(math.log2(N))
    # LRI.sort(key=lambda x: hilbert_order(x[0], x[1], p))
    for l, r, i in LRI:
        # ans[i] = ...
        pass
