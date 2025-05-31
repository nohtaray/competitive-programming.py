def monotone_minima(N, min_j, max_j, fn):
    """
    Monotone Minima
    monotone な行列の各行 i に対して、j の範囲 [min_j, max_j] で最小値を求める
    M = max_j - min_j として O(N+M log N)
    https://atcoder.jp/contests/abc408/submissions/66369353
    :param N: 行数
    :param min_j: j が取る最小値
    :param max_j: j が取る最大値
    :param fn: fn(i, j) -> i 行 j 列の値
               i の増加に対して、最小値を取る j が広義単調増加であること
               i <= j など条件があるとき、範囲内の戻り値が範囲外の戻り値より小さくなるように注意 https://www.notion.so/Monotone-Minima-204cc6adacf0809a8ee7ff7462ad03fa?source=copy_link
    """
    INF = float("inf")
    ans = [INF] * N
    stack = [(0, N, min_j, max_j)]
    while stack:
        li, ri, min_j, max_j = stack.pop()
        mi = (li + ri) // 2
        opt_a = INF
        opt_j = min_j
        for j in range(min_j, max_j + 1):
            v = fn(mi, j)
            if v < opt_a:
                opt_a = v
                opt_j = j
        ans[mi] = opt_a
        if li < mi:
            stack.append((li, mi, min_j, opt_j))
        if mi + 1 < ri:
            stack.append((mi + 1, ri, opt_j, max_j))
    return ans
