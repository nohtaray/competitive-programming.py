def fast_zeta_transform(counts, size):
    """
    高速ゼータ変換
    ret[s]: sum of counts[t] (t ⊆ s)
    https://qiita.com/Euglenese/items/260f9ddf513f772d7e42#本題
    O(2^N * N); len(counts) == 2^N
    :param list of int counts:
    :param int size:
    """
    assert (1 << size) == len(counts)
    dp = list(counts)
    for j in range(size):
        for i in range(1 << size):
            if i & (1 << j):
                dp[i] += dp[i & ~(1 << j)]
    return dp


def min_coloring_count(graph):
    """
    隣接する頂点同士の色を変えるときの最小の彩色数 O(2^N * N * logN)
    https://www.slideshare.net/wata_orz/ss-12208032
    Verify: https://atcoder.jp/contests/tenka1-2014-quala/submissions/11676865
    :param list of (list of int) graph:
    """
    N = len(graph)
    # v から u に辺があれば mat[v] >> u & 1 == 1
    mat = [0] * N
    for v in range(len(graph)):
        mat[v] |= 1 << v
        for u in graph[v]:
            mat[v] |= 1 << u
            mat[u] |= 1 << v

    # is_independent[s]: s が独立集合なら 1
    is_independent = [0] * (1 << N)
    is_independent[0] = 1
    for s in range(1 << N):
        if not is_independent[s]:
            continue
        for b in range(N):
            # b と隣接する頂点が s に含まれない
            if mat[b] & s == 0:
                is_independent[s | (1 << b)] = 1
    is_independent[0] = 0

    # k == 1 の場合: 普通の高速ゼータ変換
    # counts[s]: 集合 s の部分集合として独立集合をとる方法が何通りあるか
    counts = fast_zeta_transform(is_independent, size=N)

    # B[i]: i に立ってるビット数
    B = []
    for i in range(1 << N):
        b = 0
        while i > 0:
            b += i & 1
            i >>= 1
        B.append(b)

    def test(k):
        """
        k 個の独立集合の和集合のサイズを N にできるか == S の独立集合たちを k 色で彩色可能か
        O(2^N * N)
        :param int k:
        """
        # https://www.slideshare.net/wata_orz/ss-12208032
        # P.21
        # f(S): S の部分集合から独立集合を k 個選ぶ数 == I(S)^k
        # g(S): そのうち S を覆う数 == 上記から S を覆わない数を引く
        #       == f(S) + sum of ( (-1)^(|S|-|T|) * f(T) ) (T ⊂ S)
        #       ==        sum of ( (-1)^(|S|-|T|) * f(T) ) (T ⊆ S)
        operands = [0] * len(counts)
        for t in range(len(operands)):
            f_t = pow(counts[t], k)  # f(T)
            sign = (-1) ** (N - B[t])  # |S| == N
            operands[t] = sign * f_t
        patterns = fast_zeta_transform(operands, size=N)
        return patterns[-1] > 0

    ok = N
    ng = 0
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if test(mid):
            ok = mid
        else:
            ng = mid
    return ok
