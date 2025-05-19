import heapq
from typing import List, Tuple


def minimum_steiner_tree_dense(
    graph: List[List[int]], terminals: List[int]
) -> (int, List[List[int]]):
    """
    無向グラフの最小シュタイナー木 (密グラフ用)
    K をターミナル数として O(3^K V + 2^K V^2)
    Verify: https://atcoder.jp/contests/abc395/submissions/63326997
    :param graph: 隣接行列
    :param terminals: ターミナルとなる頂点
    :returns: 最小コスト, dp 配列 (dp[s][v]: s と v を含むグラフの最小コスト)
    """
    INF = float("inf")
    N = len(graph)
    K = len(terminals)

    # t2s[v]: v がターミナルに含まれるときのビット
    t2s = [-1] * N
    for i, v in enumerate(terminals):
        t2s[v] = 1 << i

    # dp[s][v]: s と v を含むグラフの最小コスト
    dp = [[INF] * N for _ in range(1 << K)]
    for s in range(1 << K):
        for v in range(N):
            if s == 0 or s == t2s[v]:
                dp[s][v] = 0
                continue
            t = s
            while t > 0:
                dp[s][v] = min(dp[s][v], dp[t][v] + dp[s ^ t][v])
                t = (t - 1) & s

        dist = dp[s]
        seen = [False] * N
        for _ in range(N):
            mv = -1
            md = INF
            for v in range(N):
                if dist[v] < md and not seen[v]:
                    mv = v
                    md = dist[v]
            v = mv
            d = md
            for u in range(N):
                dist[u] = min(dist[u], d + graph[v][u])
            seen[v] = True
    return min(dp[-1]), dp


def minimum_steiner_tree_sparse(
    graph: List[List[Tuple[int, int]]], terminals: List[int]
) -> (int, List[List[int]]):
    """
    無向グラフの最小シュタイナー木 (疎グラフ用)
    K をターミナル数として O(3^K V + 2^K (V+E)logE)
    Verify: https://atcoder.jp/contests/abc395/submissions/63326997
    重たいので C++ 推奨: https://atcoder.jp/contests/abc364/submissions/63327948
    :param graph: 隣接リスト
    :param terminals: ターミナルとなる頂点
    :returns: 最小コスト, dp 配列 (dp[s][v]: s と v を含むグラフの最小コスト)
    """
    INF = float("inf")
    N = len(graph)
    K = len(terminals)

    # t2s[v]: v がターミナルに含まれるときのビット
    t2s = [-1] * N
    for i, v in enumerate(terminals):
        t2s[v] = 1 << i

    # dp[s][v]: s と v を含むグラフの最小コスト
    dp = [[INF] * N for _ in range(1 << K)]
    for s in range(1 << K):
        for v in range(N):
            if s == 0 or s == t2s[v]:
                dp[s][v] = 0
                continue
            t = s
            while t > 0:
                dp[s][v] = min(dp[s][v], dp[t][v] + dp[s ^ t][v])
                t = (t - 1) & s

        dist = dp[s]
        heap = []
        for v in range(N):
            heap.append((dist[v], v))
        heapq.heapify(heap)
        while heap:
            d, v = heapq.heappop(heap)
            if d > dist[v]:
                continue
            for u, c in graph[v]:
                if d + c >= dist[u]:
                    continue
                dist[u] = d + c
                heapq.heappush(heap, (dist[u], u))
    return min(dp[-1]), dp
