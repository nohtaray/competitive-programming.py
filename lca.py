import math


class BisectLCA:
    """
    LCA 二分探索版
    初期化 O(NlogN)、クエリ O(logN)
    """

    def __init__(self, graph, max_v, root):
        """
        :param list of (list of int) graph:
        :param int max_v:
        :param int root:
        """
        self.graph = graph
        self.size = max_v + 1
        self.root = root

        self.MAX_LOG_V = math.floor(math.log2(self.size)) + 1
        # depths[v]: v の root からの距離
        self.depths = [-1] * self.size
        # parents[k][v]: 親に 2^k たどった頂点
        self.parents = [[-1] * self.size for _ in range(self.MAX_LOG_V)]

        self._init()

    def _init(self):
        # depths と parents[0] を初期化
        stack = [(self.root, 0, -1)]
        while stack:
            v, d, par = stack.pop()
            self.parents[0][v] = par
            self.depths[v] = d
            for u in self.graph[v]:
                stack.append((u, d + 1, v))

        # 各 parents を初期化
        for k in range(self.MAX_LOG_V - 1):
            for v in range(self.size):
                if self.parents[k][v] < 0:
                    # 親がなければ -1
                    self.parents[k + 1][v] = -1
                else:
                    self.parents[k + 1][v] = self.parents[k][self.parents[k][v]]

    def lca(self, u, v):
        # 深さを合わせる
        if self.depths[u] > self.depths[v]:
            u, v = v, u
        for k in range(self.MAX_LOG_V):
            if (self.depths[v] - self.depths[u]) >> k & 1:
                v = self.parents[k][v]
        if v == u:
            return v

        # にぶたん
        for k in reversed(range(self.MAX_LOG_V)):
            if self.parents[k][u] != self.parents[k][v]:
                u = self.parents[k][u]
                v = self.parents[k][v]
        return self.parents[0][u]
