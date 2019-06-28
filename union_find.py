class UnionFind:
    def __init__(self, size=None, nodes=None):
        """
        size か nodes どっちか指定。
        nodes は set、size は list を使う。
        set の最悪計算量は O(N) なので size 指定のほうが若干速い
        :param int size:
        :param collections.Iterable nodes:
        """
        assert size is not None or nodes is not None
        if size is not None:
            self._parents = [i for i in range(size)]
            self._ranks = [0 for _ in range(size)]
            self._sizes = [1 for _ in range(size)]
        else:
            self._parents = {k: k for k in nodes}
            self._ranks = {k: 0 for k in nodes}
            self._sizes = {k: 1 for k in nodes}

    def unite(self, x, y):
        """
        x が属する木と y が属する木を併合
        :param x:
        :param y:
        :return:
        """
        x = self.root(x)
        y = self.root(y)
        if x == y:
            return

        # rank が小さい方が下
        if self._ranks[x] > self._ranks[y]:
            # x が root
            self._parents[y] = x
            self._sizes[x] += self._sizes[y]
        else:
            # y が root
            self._parents[x] = y
            self._sizes[y] += self._sizes[x]
            if self._ranks[x] == self._ranks[y]:
                self._ranks[y] += 1

    def root(self, x):
        """
        x が属する木の root
        :param x:
        :return:
        """
        if self._parents[x] == x:
            return x
        self._parents[x] = self.root(self._parents[x])
        return self._parents[x]

    def size(self, x):
        """
        x が属する木のノード数
        :param x:
        :return:
        """
        return self._sizes[self.root(x)]


class WeightedUnionFind:
    def __init__(self, size=None, nodes=None):
        """
        size か nodes どっちか指定。
        nodes は set、size は list を使う。
        set の最悪計算量は O(N) なので size 指定のほうが若干速い
        :param int size:
        :param collections.Iterable nodes:
        """
        assert size is not None or nodes is not None
        if size is not None:
            self._parents = [i for i in range(size)]
            self._ranks = [0 for _ in range(size)]
            self._sizes = [1 for _ in range(size)]
            # 直近の親からの重み。root なら 0
            self._weights = [0 for _ in range(size)]
        else:
            self._parents = {k: k for k in nodes}
            self._ranks = {k: 0 for k in nodes}
            self._sizes = {k: 1 for k in nodes}
            # 直近の親からの重み。root なら 0
            self._weights = {k: 0 for k in nodes}

    def unite(self, x, y, w):
        """
        x が属する木と y が属する木を併合
        :param x:
        :param y:
        :param w: x と y の重みの差; (重み y) - (重み x)
        :return:
        """
        rx = self.root(x)
        ry = self.root(y)
        if rx == ry:
            return

        # rank が小さい方が下
        if self._ranks[rx] > self._ranks[ry]:
            # x が root
            self._parents[ry] = rx
            self._sizes[rx] += self._sizes[ry]
            # root 間の重みに変換
            self._weights[ry] = w + self._weights[x] - self._weights[y]
        else:
            # y が root
            self._parents[rx] = ry
            self._sizes[ry] += self._sizes[rx]
            # root 間の重みに変換
            self._weights[rx] = -w + self._weights[y] - self._weights[x]
            if self._ranks[rx] == self._ranks[ry]:
                self._ranks[ry] += 1

    def root(self, x):
        """
        x が属する木の root
        :param x:
        :return:
        """
        if self._parents[x] == x:
            return x
        root = self.root(self._parents[x])
        self._weights[x] += self._weights[self._parents[x]]
        self._parents[x] = root
        return root

    def size(self, x):
        """
        x が属する木のノード数
        :param x:
        :return:
        """
        return self._sizes[self.root(x)]

    def weight(self, x):
        """
        :param x:
        :return:
        """
        # 経路圧縮
        self.root(x)
        return self._weights[x]

    def diff(self, x, y):
        """
        (y の重み) - (x の重み)
        :param x:
        :param y:
        :return:
        """
        if self.root(x) == self.root(y):
            return self._weights[y] - self._weights[x]
        return float("inf")


if __name__ == "__main__":
    uf = UnionFind(nodes=[i for i in range(10)])

    assert uf.root(0) == 0
    assert uf.root(1) == 1

    uf.unite(1, 2)
    uf.unite(3, 4)
    uf.unite(1, 4)
    uf.unite(7, 8)
    assert uf.root(3) == uf.root(2)
    assert uf.root(1) != uf.root(7)
    assert uf.size(1) == uf.size(2) == uf.size(3) == uf.size(4) == 4
    assert uf.size(7) == uf.size(8) == 2
    assert uf.size(5) == 1

    uf2 = UnionFind(nodes=["a", "b", "c", "d", "e"])
    uf2.unite("a", "e")
    uf2.unite("c", "e")
    assert uf2.root("a") == uf2.root("c")
    assert uf2.root("b") != uf2.root("e")
