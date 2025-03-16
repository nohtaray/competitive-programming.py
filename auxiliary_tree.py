from collections import defaultdict
from typing import List, Tuple, Dict

from libs.lca import DoublingLCA


class AuxiliaryTree:
    def __init__(self, graph, root):
        """
        グラフのサイズを N、頂点集合のサイズを K として、
        - 前処理 O(N)
        - 構築 O(K log K)
        :param list of (list of int) graph:
        :param int root:
        """
        N = len(graph)
        # 行きがけ順
        pre_order = []
        seen = [False] * N
        seen[root] = True
        depths = [-1] * N
        depths[root] = 0
        # (v, depth)
        stack = [(root, 0)]
        while stack:
            v, d = stack.pop()
            pre_order.append(v)
            depths[v] = d
            for u in graph[v]:
                if seen[u]:
                    continue
                seen[u] = True
                depths[u] = d + 1
                stack.append((u, d + 1))

        o2v = pre_order
        v2o = [-1] * N
        for i, v in enumerate(o2v):
            v2o[v] = i

        self._graph = graph
        self._root = root
        self._o2v = o2v
        self._v2o = v2o
        self._depths = depths
        self._lca = DoublingLCA(graph, root)

    def build(self, V) -> Tuple[List[int], List[Tuple[int, int]], Dict[int, List[int]]]:
        """
        V に含まれる頂点からなる auxiliary tree を構築
        O(|V|log|V|)
        :param list of int V:
        :return: (使う頂点のリスト, 辺のリスト, graph)
        """
        # https://smijake3.hatenablog.com/entry/2019/09/15/200200#ソート1回の方法
        # 行きがけ順でソート
        V = list(sorted(V, key=lambda v: self._v2o[v]))
        visited = list(V)
        parents = defaultdict(int)
        parents[V[0]] = -1
        stack = [V[0]]
        for i in range(1, len(V)):
            lca = self._lca.lca(stack[-1], V[i])
            while stack and self._depths[stack[-1]] >= self._depths[lca]:
                u = stack.pop()
                if stack and self._depths[stack[-1]] >= self._depths[lca]:
                    parents[u] = stack[-1]
                else:
                    parents[u] = lca
            stack.append(lca)
            stack.append(V[i])
            visited.append(lca)
        parents[stack[0]] = -1
        for v, u in zip(stack, stack[1:]):
            parents[u] = v

        ret_verts = list(set(visited))
        ret_edges = []
        ret_graph = defaultdict(list)
        for v in ret_verts:
            if parents[v] == -1:
                continue
            ret_edges.append((v, parents[v]))
            ret_graph[v].append(parents[v])
            ret_graph[parents[v]].append(v)
        return ret_verts, ret_edges, ret_graph
