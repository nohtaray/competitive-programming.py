import atcoder.fenwicktree


class Map:
    """
    重複なしのソートされた整数列
    左右からの pop が O(log^2 N)
    Verify (TLE): https://atcoder.jp/contests/abc406/submissions/65945423
    """

    def __init__(self, n):
        self._n = n
        self._ft = atcoder.fenwicktree.FenwickTree(n)
        self._left = None
        self._right = None
        self._hist = []

    def add(self, i, add_hist=True):
        if self._ft.sum(i, i + 1) > 0:
            return
        self._ft.add(i, 1)
        if add_hist:
            self._hist.append((i, 1))
        if self._left is not None and i < self._left:
            self._left = i
        if self._right is not None and i > self._right:
            self._right = i

    def remove(self, i, add_hist=True):
        if self._ft.sum(i, i + 1) == 0:
            raise ValueError("remove from empty deque")
        self._ft.add(i, -1)
        if add_hist:
            self._hist.append((i, -1))
        if self._left == i:
            self._left = None
        if self._right == i:
            self._right = None

    def contains(self, i):
        return self._ft.sum(i, i + 1) > 0

    def count(self):
        return self._ft.sum(0, self._n)

    @property
    def hist(self):
        return self._hist

    def revert(self):
        if not self._hist:
            raise ValueError("no history")
        i, v = self._hist.pop()
        if v > 0:
            self.remove(i, False)
        else:
            self.add(i, False)

    def peek(self):
        if self._right is not None:
            return self._right
        if self.count() == 0:
            raise IndexError("pop from an empty deque")
        s = self.count()
        ok = self._n
        ng = -1
        while abs(ok - ng) > 1:
            mid = (ok + ng) // 2
            if self._ft.sum(0, mid + 1) == s:
                ok = mid
            else:
                ng = mid
        self._right = ok
        return ok

    def peekleft(self):
        if self._left is not None:
            return self._left
        if self.count() == 0:
            raise IndexError("pop from an empty deque")
        ok = self._n
        ng = -1
        while abs(ok - ng) > 1:
            mid = (ok + ng) // 2
            if self._ft.sum(0, mid + 1) > 0:
                ok = mid
            else:
                ng = mid
        self._left = ok
        return ok

    def pop(self):
        ok = self.peek()
        self.remove(ok)
        self._right = None
        return ok

    def popleft(self):
        ok = self.peekleft()
        self.remove(ok)
        self._left = None
        return ok
