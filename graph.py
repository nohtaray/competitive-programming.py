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
    return scipy.sparse.csgraph.floyd_warshall(*args, **kwargs)


def bellman_ford(*args, **kwargs):
    return scipy.sparse.csgraph.bellman_ford(*args, **kwargs)


def johnson(*args, **kwargs):
    return scipy.sparse.csgraph.johnson(*args, **kwargs)


def dijkstra(graph, start):
    """
    マイナスの辺があっちゃダメ
    scipy.sparse.csgraph.dijkstra は内部で使われてるフィボナッチヒープが一部のケースでめっちゃ遅いのであんまり使わないほうがよさげ
    https://atcoder.jp/contests/soundhound2018-summer-qual/submissions/5311823

    :param list of (list of (int, int)) graph:
        graph[from_index]: (to_index, weight)
    :param int start:
    :return:
    """
    dist = [float('inf') for _ in range(len(graph))]
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