import heapq


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


def dijkstra(graph, start):
    """
    scipy.sparse.csgraph.dijkstra は内部で使われてるフィボナッチヒープが一部のケースでめっちゃ遅いのであんまり使わないほうがよさげ
    https://atcoder.jp/contests/soundhound2018-summer-qual/submissions/5311823
    :param list of (list of (int, int)) graph:
        graph[from_index]: (to_index, weight)
    :param int start:
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


def euler_tour(tree, max_v, root=0):
    """
    木のオイラーツアー (通った頂点を順に返す)
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


def euler_tour_inout(tree, max_v, root=0):
    """
    木のオイラーツアー (頂点の出入りを順に返す)
    各頂点について、入るときと出るときの 2 回記録される
    :param list of (list of (int, int)) tree:
    :param int max_v:
    :param int root:
    :return: (trails, depths, weights)
    :rtype: (list of int, list of int, list of int)
    """
    seen = [False] * (max_v + 1)
    # 頂点の履歴 (入ったときと出たときに記録)
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

        stack.append((v, d, -w, False))
        for u, w in tree[v]:
            if not seen[u]:
                stack.append((u, d + 1, w, True))
    return trails, depths, weights


def topological_sort(graph):
    """
    :param list of (list of int) graph:
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


def enumerate_bridges(graph):
    """
    橋を列挙する
    http://nupioca.hatenadiary.jp/entry/2013/11/03/200006
    Verify: https://atcoder.jp/contests/abc075/submissions/12488523
    :param list of (list of int) graph:
    """
    N = len(graph)
    ret_bridges = []
    pres = [-1] * N
    lows = [-1] * N
    order = -1
    for v in range(N):
        if pres[v] >= 0:
            continue
        edges = [(None, v, True)]
        while edges:
            v, u, forward = edges.pop()
            if forward:
                if pres[u] >= 0:
                    # もう来たことがある
                    lows[v] = min(lows[v], lows[u])
                    continue
                edges.append((v, u, False))
                parent, v = v, u
                order += 1
                pres[v] = lows[v] = order
                for u in graph[v]:
                    if u == parent:
                        continue
                    edges.append((v, u, True))
            else:
                if v is None:
                    continue
                if lows[u] == pres[u]:
                    ret_bridges.append((v, u))
                lows[v] = min(lows[v], lows[u])
    return ret_bridges


def strongly_connected_components(graph):
    """
    強連結成分分解; SCC
    ret[v]: v のコンポーネント番号
    コンポーネント番号はトポロジカル順で前にある方が小さい
    Verify: https://atcoder.jp/contests/arc030/submissions/14035565
    Verify: http://judge.u-aizu.ac.jp/onlinejudge/review.jsp?rid=4553151#1
    :param list of (list of int) graph:
    :rtype: list of int
    """
    N = len(graph)

    rev_graph = [[] for _ in range(N)]
    for v in range(N):
        for u in graph[v]:
            rev_graph[u].append(v)

    # 帰りがけ順
    pre_order = []
    seen = [False] * N
    for v in range(N):
        if seen[v]:
            continue
        seen[v] = True
        stack = [(v, 0)]
        while stack:
            v, pos = stack.pop()
            for i in range(pos, len(graph[v])):
                u = graph[v][i]
                if seen[u]:
                    continue
                seen[u] = True
                # 中断して次の頂点を Stack に詰む
                stack.append((v, i + 1))
                stack.append((u, 0))
                break
            else:
                # 帰りがけ
                pre_order.append(v)

    # 帰りがけ順が遅い順に DFS
    cid = 0
    ret = [-1] * N
    seen = [False] * N
    for v in reversed(pre_order):
        if seen[v]:
            continue
        seen[v] = True
        stack = [v]
        while stack:
            v = stack.pop()
            ret[v] = cid
            for u in rev_graph[v]:
                if seen[u]:
                    continue
                seen[u] = True
                stack.append(u)
        cid += 1
    return ret
