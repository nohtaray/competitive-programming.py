class UnionFind:
    def __init__(self, nodes):
        """
        :param collections.Iterable nodes:
        """
        self._parents = {k: k for k in nodes}
        self._ranks = {k: 0 for k in nodes}
        self._sizes = {k: 1 for k in nodes}

    def union(self, x, y):
        """
        x が属する木と y が属する木を併合
        :param x:
        :param y:
        :return:
        """
        x = self.find(x)
        y = self.find(y)
        if x != y:
            # rank が小さい方が下
            if self._ranks[x] > self._ranks[y]:
                self._parents[y] = x
                self._sizes[x] += self._sizes[y]
            else:
                self._parents[x] = y
                self._sizes[y] += self._sizes[x]
                if self._ranks[x] == self._ranks[y]:
                    self._ranks[y] += 1

    def find(self, x):
        """
        x が属する木の root
        :param x:
        :return:
        """
        if self._parents[x] == x:
            return x
        self._parents[x] = self.find(self._parents[x])
        return self._parents[x]

    def size(self, x):
        """
        x が属する木のノード数
        :param x:
        :return:
        """
        return self._sizes[self.find(x)]


if __name__ == '__main__':
    uf = UnionFind(nodes=[i for i in range(10)])

    assert uf.find(0) == 0
    assert uf.find(1) == 1

    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(1, 4)
    uf.union(7, 8)
    assert uf.find(3) == uf.find(2)
    assert uf.find(1) != uf.find(7)
    assert uf.size(1) == uf.size(2) == uf.size(3) == uf.size(4) == 4
    assert uf.size(7) == uf.size(8) == 2
    assert uf.size(5) == 1

    uf2 = UnionFind(nodes=['a', 'b', 'c', 'd', 'e'])
    uf2.union('a', 'e')
    uf2.union('c', 'e')
    assert uf2.find('a') == uf2.find('c')
    assert uf2.find('b') != uf2.find('e')
