import heapq

import scipy.sparse.csgraph


# scipy.sparse.csgraph 使える
# https://docs.scipy.org/doc/scipy/reference/sparse.csgraph.html

# 疎行列の使い分けはこれ参考になる
# http://kaisk.hatenadiary.com/entry/2014/04/11/202823

# floyd_warshall: O(V^3)。全点最短路問題用。
# bellman_ford: indices で始点固定すれば O(VE)。
# dijkstra: O(E log V)。改良版 Bellman-Ford。重みが負の辺があるとダメ。
# johnson: O(V^2 log V + VE)。重みが負の辺はあってもいいが、負の閉路があるとダメ。Floyd-Warshall よりちょっと速い。


def floyd_warshall(*args, **kwargs):
    """
    これでもよさそう
    https://atcoder.jp/contests/abc051/submissions/6148260
    :param args:
    :param kwargs:
    :return:
    """
    return scipy.sparse.csgraph.floyd_warshall(*args, **kwargs)


def bellman_ford(graph, from_v, to_v):
    """
    到達できないなら INF、負閉路があったら -INF
    :param list of (list of (int, int)) graph: (to, cap) の隣接リスト
    :param int from_v:
    :param int to_v:
    :rtype: int
    """

    def reachable(graph, from_v):
        """
        graph 上で from_v から到達できるかどうかのリスト
        :param graph:
        :param from_v:
        """
        ret = [False] * len(graph)
        ret[from_v] = True
        stack = [from_v]
        while stack:
            v = stack.pop()
            for u, _ in graph[v]:
                if not ret[u]:
                    ret[u] = True
                    stack.append(u)
        return ret

    # from_v から到達でき、かつ to_v へ到達できる頂点のみ考える
    # これら以外には負閉路があっても関係ない
    vertices = []
    revs = [[] for _ in range(len(graph))]
    for v, ud in enumerate(graph):
        for u, d in ud:
            revs[u].append((v, d))
    for v, (r1, r2) in enumerate(zip(reachable(graph, from_v), reachable(revs, to_v))):
        if r1 & r2:
            vertices.append(v)

    dist = [float('inf')] * len(graph)
    dist[from_v] = 0
    updated = True
    for _ in range(len(graph) + 1):
        updated = False
        for v in vertices:
            for u, d in graph[v]:
                if dist[v] + d < dist[u]:
                    dist[u] = dist[v] + d
                    updated = True
        if not updated:
            break
    return -float('inf') if updated else dist[to_v]


def johnson(*args, **kwargs):
    return scipy.sparse.csgraph.johnson(*args, **kwargs)


def dijkstra(graph, start):
    """
    TODO: start 指定しなかったら全部の距離を知りたい

    マイナスの辺があっちゃダメ
    scipy.sparse.csgraph.dijkstra は内部で使われてるフィボナッチヒープが一部のケースでめっちゃ遅いのであんまり使わないほうがよさげ
    https://atcoder.jp/contests/soundhound2018-summer-qual/submissions/5311823

    :param list of (list of (int, int)) graph:
        graph[from_index]: (to_index, weight)
    :param int start:
    :return:
    """
    dist = [float("inf") for _ in range(len(graph))]
    dist[start] = 0
    heap = []
    heapq.heappush(heap, (0, start))

    while len(heap) > 0:
        w, v = heapq.heappop(heap)
        if w > dist[v]:
            continue
        for u, dw in graph[v]:
            if w + dw < dist[u]:
                dist[u] = w + dw
                heapq.heappush(heap, (w + dw, u))
    return dist


def eulerian_trail(tree, max_v, root=0):
    """
    木のオイラー路; オイラーツアー
    :param list of (list of (int, int)) tree:
    :param int max_v:
    :param int root:
    :return: (trails, depths, weights)
    :rtype: (list of int, list of int, list of int)
    """
    seen = [False] * (max_v + 1)
    # 頂点の履歴
    trails = []
    # 深さの履歴
    depths = []
    # 距離の履歴
    weights = []
    # Overflow 回避のためループで
    stack = [(root, 0, 0, True)]
    while stack:
        v, d, w, forward = stack.pop()
        seen[v] = True
        trails.append(v)
        depths.append(d)
        weights.append(w)
        if not forward:
            continue

        for u, w in tree[v]:
            if not seen[u]:
                stack.append((v, d, -w, False))
                stack.append((u, d + 1, w, True))
    return trails, depths, weights


def topological_sort(graph):
    """
    :param list of (list of int) graph:
    :return:
    """
    # 入次数
    ins = [0] * len(graph)
    for vs in graph:
        for v in vs:
            ins[v] += 1

    # 入次数がゼロのやつ
    zeros = []
    for v, cnt in enumerate(ins):
        if cnt == 0:
            zeros.append(v)

    # 入次数がゼロのやつから順に追加してく
    ret = []
    while zeros:
        v = zeros.pop()
        ret.append(v)
        for u in graph[v]:
            ins[u] -= 1
            if ins[u] == 0:
                zeros.append(u)

    if len(ret) != len(graph):
        raise ValueError('閉路があります')

    return ret
