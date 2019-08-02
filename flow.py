from collections import deque, defaultdict


class Dinic:
    def __init__(self, graph=None, residual=None):
        """
        :param list of (list of (int, int)) graph: (to, cap) の隣接リスト
        :param list of (list of (list of (int|list))) residual: (to, cap, rev) の残余グラフ
        """
        assert (graph and not residual) or (not graph and residual)
        if graph:
            self.graph = self.residual_graph(graph)
        else:
            self.graph = residual

    @staticmethod
    def residual_graph(graph):
        """
        残余グラフ構築
        :param list of (list of (int, int)) graph: (to, cap) の隣接リスト
        :rtype: list of (list of (list of (int|list)))
        :return: (to, cap, rev) の残余グラフ
        """
        ret = [[] for _ in range(len(graph))]
        for v in range(len(graph)):
            for u, cap in graph[v]:
                rev = [v, 0]
                edge = [u, cap, rev]
                rev.append(edge)
                ret[v].append(edge)
                ret[u].append(rev)
        return ret

    def _dist(self, s):
        """
        :param int s:
        :rtype: list of int
        :return: s からの距離。残余グラフ上で到達できない場合は -1
        """
        ret = [-1] * len(self.graph)
        ret[s] = 0
        que = deque([(s, 0)])
        while que:
            v, d = que.popleft()
            for u, cap, _ in self.graph[v]:
                if ret[u] < 0 < cap:
                    ret[u] = d + 1
                    que.append((u, d + 1))
        return ret

    def _dfs(self, s, t, dist, iter, flow=float('inf')):
        """
        :param int s:
        :param int t:
        :param list of int dist:
        :param list of int iter:
        :param int flow:
        """
        if s == t:
            return flow
        while iter[s] < len(self.graph[s]):
            edge = self.graph[s][iter[s]]
            to, cap, rev = edge
            if dist[s] < dist[to] and cap > 0:
                f = self._dfs(to, t, dist, iter, min(flow, cap))
                if f > 0:
                    edge[1] -= f
                    rev[1] += f
                    return f
            iter[s] += 1
        return 0

    def maximum_flow(self, from_v, to_v):
        """
        :param int from_v:
        :param int to_v:
        :return: from_v から to_v への最大流
        """
        ret = 0
        while True:
            dist = self._dist(from_v)
            if dist[to_v] < 0:
                break
            iter = [0] * len(self.graph)
            while True:
                flow = self._dfs(from_v, to_v, dist, iter)
                if flow == 0:
                    break
                ret += flow
        return ret


class DictDinic:
    """
    Dinic の頂点を int 以外でもいいようにしたやつ
    """

    def __init__(self, graph=None, residual=None):
        """
        :param dict[Any, (list of (Any, int))] graph: (to, cap) の隣接リスト
        :param dict[Any, (list of list)] residual: (to, cap, rev) の残余グラフ
        """
        assert (graph and not residual) or (not graph and residual)
        if graph:
            self.graph = self.residual_graph(graph)
        else:
            self.graph = residual

    @staticmethod
    def residual_graph(graph):
        """
        残余グラフ構築
        :param dict[Any, (list of (Any, int))] graph: (to, cap) の隣接リスト
        :rtype: dict[Any, (list of list)]
        :return: (to, cap, rev) の残余グラフ
        """
        ret = defaultdict(list)
        for v in graph.keys():
            for u, cap in graph[v]:
                rev = [v, 0]
                edge = [u, cap, rev]
                rev.append(edge)
                ret[v].append(edge)
                ret[u].append(rev)
        return ret

    def _dist(self, s):
        """
        :param s:
        :rtype: dict[Any, int]
        :return: s からの距離。残余グラフ上で到達できない場合は -1
        """
        ret = defaultdict(lambda: -1)
        ret[s] = 0
        que = deque([(s, 0)])
        while que:
            v, d = que.popleft()
            for u, cap, _ in self.graph[v]:
                if ret[u] < 0 < cap:
                    ret[u] = d + 1
                    que.append((u, d + 1))
        return ret

    def _dfs(self, s, t, dist, iter, flow=float('inf')):
        """
        :param s:
        :param t:
        :param dict[Any, int] dist:
        :param dict[Any, int] iter:
        :param int flow:
        """
        if s == t:
            return flow
        while iter[s] < len(self.graph[s]):
            edge = self.graph[s][iter[s]]
            to, cap, rev = edge
            if dist[s] < dist[to] and cap > 0:
                f = self._dfs(to, t, dist, iter, min(flow, cap))
                if f > 0:
                    edge[1] -= f
                    rev[1] += f
                    return f
            iter[s] += 1
        return 0

    def maximum_flow(self, from_v, to_v):
        """
        :param from_v:
        :param to_v:
        :return: from_v から to_v への最大流
        """
        ret = 0
        while True:
            dist = self._dist(from_v)
            if dist[to_v] < 0:
                break
            iter = defaultdict(int)
            while True:
                flow = self._dfs(from_v, to_v, dist, iter)
                if flow == 0:
                    break
                ret += flow
        return ret


class MinCostFlow:
    """
    最小費用流 ベルマンフォード版
    """

    def __init__(self, graph=None, residual=None):
        """
        :param list of (list of (int, int, int)) graph: (to, cap, cost) の隣接リスト
        :param list of (list of (list of (int|list))) residual: (to, cap, cost, rev) の残余グラフ
        """
        assert (graph and not residual) or (not graph and residual)
        if graph:
            self.graph = self.residual_graph(graph)
        else:
            self.graph = residual

    @staticmethod
    def residual_graph(graph):
        """
        残余グラフ構築
        :param list of (list of (int, int, int)) graph: (to, cap, cost) の隣接リスト
        :rtype: list of (list of (list of (int|list)))
        :return: (to, cap, cost, rev) の残余グラフ
        """
        ret = [[] for _ in range(len(graph))]
        for v in range(len(graph)):
            for u, cap, cost in graph[v]:
                rev = [v, 0, -cost]
                edge = [u, cap, cost, rev]
                rev.append(edge)
                ret[v].append(edge)
                ret[u].append(rev)
        return ret

    def solve(self, from_v, to_v, flow):
        """
        :param int from_v:
        :param int to_v:
        :param int flow:
        :rtype: int
        """
        remains = flow
        total_cost = 0
        while remains > 0:
            # 最短路
            dist = [float('inf')] * len(self.graph)
            preve = [None] * len(self.graph)
            prevv = [None] * len(self.graph)
            dist[from_v] = 0
            stop = False
            while not stop:
                stop = True
                for v, edges in enumerate(self.graph):
                    for edge in edges:
                        u, cap, cost, rev = edge
                        if cap > 0 and dist[v] + cost < dist[u]:
                            dist[u] = dist[v] + cost
                            prevv[u] = v
                            preve[u] = edge
                            stop = False
            flow = remains
            if dist[to_v] == float('inf'):
                total_cost = -1
                break

            v = to_v
            while v != from_v:
                cap = preve[v][1]
                v = prevv[v]
                flow = min(cap, flow)

            # path に沿って flow 流す
            cost = 0
            v = to_v
            while v != from_v:
                cost += preve[v][2] * flow
                preve[v][1] -= flow
                preve[v][3][1] += flow
                v = prevv[v]

            remains -= flow
            total_cost += cost
        return total_cost


class DictMinCostFlow:
    """
    最小費用流 ベルマンフォード版
    MinCostFlow の頂点を int 以外でもいいようにしたやつ。
    """

    def __init__(self, graph=None, residual=None):
        """
        :param dict[Any, (list of (Any, int, int))] graph: (to, cap, cost) の隣接リスト
        :param dict[Any, (list of list)] residual: (to, cap, cost, rev) の残余グラフ
        """
        assert (graph and not residual) or (not graph and residual)
        if graph:
            self.graph = self.residual_graph(graph)
        else:
            self.graph = residual

    @staticmethod
    def residual_graph(graph):
        """
        残余グラフ構築
        :param dict[Any, (list of (Any, int, int))] graph: (to, cap, cost) の隣接リスト
        :rtype: dict[Any, (list of list)]
        :return: (to, cap, cost, rev) の残余グラフ
        """
        ret = defaultdict(list)
        for v in graph.keys():
            for u, cap, cost in graph[v]:
                rev = [v, 0, -cost]
                edge = [u, cap, cost, rev]
                rev.append(edge)
                ret[v].append(edge)
                ret[u].append(rev)
        return ret

    def solve(self, from_v, to_v, flow):
        """
        :param from_v:
        :param to_v:
        :param int flow:
        :return:
        """
        remains = flow
        total_cost = 0
        while remains > 0:
            # 最短路
            dist = defaultdict(lambda: float('inf'))
            preve = defaultdict(lambda: None)
            prevv = defaultdict(lambda: None)
            dist[from_v] = 0
            stop = False
            while not stop:
                stop = True
                for v, edges in self.graph.items():
                    for edge in edges:
                        u, cap, cost, rev = edge
                        if cap > 0 and dist[v] + cost < dist[u]:
                            dist[u] = dist[v] + cost
                            prevv[u] = v
                            preve[u] = edge
                            stop = False
            flow = remains
            if dist[to_v] == float('inf'):
                total_cost = -1
                break

            v = to_v
            while v != from_v:
                cap = preve[v][1]
                v = prevv[v]
                flow = min(cap, flow)

            # path に沿って flow 流す
            cost = 0
            v = to_v
            while v != from_v:
                cost += preve[v][2] * flow
                preve[v][1] -= flow
                preve[v][3][1] += flow
                v = prevv[v]

            remains -= flow
            total_cost += cost
        return total_cost
