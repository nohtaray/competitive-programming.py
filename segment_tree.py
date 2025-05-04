import operator
from collections import defaultdict
from functools import reduce


class SegmentTree:
    # http://codeforces.com/blog/entry/18051
    def __init__(self, values, op=operator.add):
        """
        :param list values:
        :param callable op: 結合律を満たす二項演算
        """
        self._size = len(values)
        self._op = op
        tree = [None] * self._size * 2
        tree[self._size:] = values[:]
        for i in reversed(range(1, self._size)):
            tree[i] = self._op(tree[i << 1], tree[i << 1 | 1])
        self._tree = tree

    def set(self, i, value):
        """
        values[i] = value
        :param int i:
        :param value:
        """
        i += self._size
        self._tree[i] = value
        i >>= 1
        while i > 0:
            self._tree[i] = self._op(self._tree[i << 1], self._tree[i << 1 | 1])
            i >>= 1

    def add(self, i, value):
        """
        values[i] = values[i]・value
        :param int i:
        :param value:
        """
        new_value = self._op(self._tree[self._size + i], value)
        self.set(i, new_value)

    def get(self, l, r=None):
        """
        [l, r) に op を順番に適用した値
        :param int l:
        :param int|None r:
        """
        if r is None:
            return self._tree[self._size + l]
        ret_l = []
        ret_r = []
        l += self._size
        r += self._size
        while l < r:
            if l & 1:
                ret_l.append(self._tree[l])
                l += 1
            if r & 1:
                r -= 1
                ret_r.append(self._tree[r])
            l >>= 1
            r >>= 1
        return reduce(self._op, ret_l + ret_r)

    def get_values_copy(self):
        """
        O(N) で全部の値を取得
        """
        return self._tree[self._size:]

    def __len__(self):
        return self._size


class DynamicSegmentTree:
    def __init__(self, size, e, op=operator.add):
        """
        セグ木の配列を defaultdict に変えただけ
        おっそいので使用非推奨
        後日ちゃんと実装するか C++ に変換して使う
        https://atcoder.jp/contests/abc403/submissions/65324407
        """
        self._size = size
        self._op = op
        self._tree = defaultdict(lambda: e)

    def set(self, i, value):
        """
        values[i] = value
        :param int i:
        :param value:
        """
        i += self._size
        self._tree[i] = value
        i >>= 1
        while i > 0:
            self._tree[i] = self._op(self._tree[i << 1], self._tree[i << 1 | 1])
            i >>= 1

    def add(self, i, value):
        """
        values[i] = values[i]・value
        :param int i:
        :param value:
        """
        new_value = self._op(self._tree[self._size + i], value)
        self.set(i, new_value)

    def get(self, l, r=None):
        """
        [l, r) に op を順番に適用した値
        :param int l:
        :param int|None r:
        """
        if r is None:
            return self._tree[self._size + l]
        ret_l = []
        ret_r = []
        l += self._size
        r += self._size
        while l < r:
            if l & 1:
                ret_l.append(self._tree[l])
                l += 1
            if r & 1:
                r -= 1
                ret_r.append(self._tree[r])
            l >>= 1
            r >>= 1
        return reduce(self._op, ret_l + ret_r)


class LazySegmentTreeAddMin:
    # 区間 Add、区間 Min
    # http://codeforces.com/blog/entry/18051
    def __init__(self, values):
        """
        :param list values:
        """
        # Add の単位元
        self._id = 0
        self._size = len(values)
        self._fn = min

        tree = [self._id] * self._size * 2
        tree[self._size:] = values[:]
        for i in reversed(range(1, self._size)):
            tree[i] = self._fn(tree[i << 1], tree[i << 1 | 1])
        self._tree = tree
        self._delay = [self._id] * self._size * 2

    def _add(self, p, value):
        # p 以下の子どもたちに一様に value を加算する
        # self._tree[p] は self._delay[p] を織り込み済み
        self._tree[p] += value
        if p < self._size:
            self._delay[p] += value

    def _update(self, p):
        """
        self._tree[p] の親たちを最新化する
        :param int p:
        """
        while p > 1:
            p >>= 1
            self._tree[p] = self._fn(
                self._tree[p << 1],
                self._tree[p << 1 | 1],
            ) + self._delay[p]

    def _eval(self, p):
        """
        self._tree[p] に遅延配列から値を移す
        :param int p:
        """
        # root から葉に向かって遅延配列を移していく
        for h in reversed(range(1, p.bit_length())):
            k = p >> h
            self._add(k << 1, self._delay[k])
            self._add(k << 1 | 1, self._delay[k])
            self._delay[k] = self._id

    def add(self, l, r, value):
        """
        [l, r) に value を加算する
        :param int l:
        :param int r:
        :param value:
        """
        l += self._size
        r += self._size
        l0, r0 = l, r
        while l < r:
            if l & 1:
                # 右側の子
                self._add(l, value)
                l += 1
            if r & 1:
                # 左側の子
                r -= 1
                self._add(r, value)
            l >>= 1
            r >>= 1
        self._update(l0)
        self._update(r0 - 1)

    def get(self, l, r=None):
        """
        [l, r) の Min
        :param int l:
        :param int|None r:
        """
        if r is None:
            r = l + 1
        ret_l = []
        ret_r = []
        l += self._size
        r += self._size
        self._eval(l)
        self._eval(r - 1)
        while l < r:
            if l & 1:
                ret_l.append(self._tree[l])
                l += 1
            if r & 1:
                r -= 1
                ret_r.append(self._tree[r])
            l >>= 1
            r >>= 1
        return reduce(self._fn, ret_l + ret_r[::-1])


class LazySegmentTreeAddSum:
    # 区間 Add、区間 Sum
    # http://codeforces.com/blog/entry/18051
    def __init__(self, values):
        """
        :param list values:
        """
        # Add の単位元
        self._id = 0
        self._size = len(values)
        self._fn = operator.add

        tree = [self._id] * self._size * 2
        tree[self._size:] = values[:]
        for i in reversed(range(1, self._size)):
            tree[i] = self._fn(tree[i << 1], tree[i << 1 | 1])
        self._tree = tree
        self._delay = [self._id] * self._size * 2

        children = [0] * len(self._tree)
        for i in range(self._size):
            children[~i] = 1
        for i in reversed(range(1, len(self._tree))):
            children[i >> 1] += children[i]
        self._children = children

    def _add(self, p, value):
        # p 以下の子どもたちに一様に value を加算する
        # self._tree[p] は self._delay[p] を織り込み済み
        self._tree[p] += value * self._children[p]
        if p < self._size:
            self._delay[p] += value

    def _update(self, p):
        """
        self._tree[p] の親たちを最新化する
        :param int p:
        """
        while p > 1:
            p >>= 1
            self._tree[p] = self._fn(
                self._tree[p << 1],
                self._tree[p << 1 | 1],
            ) + self._delay[p] * self._children[p]

    def _eval(self, p):
        """
        self._tree[p] に遅延配列から値を移す
        :param int p:
        """
        # root から葉に向かって遅延配列を移していく
        for h in reversed(range(1, p.bit_length())):
            k = p >> h
            self._add(k << 1, self._delay[k])
            self._add(k << 1 | 1, self._delay[k])
            self._delay[k] = self._id

    def add(self, l, r, value):
        """
        [l, r) に value を加算する
        :param int l:
        :param int r:
        :param value:
        """
        l += self._size
        r += self._size
        l0, r0 = l, r
        while l < r:
            if l & 1:
                # 右側の子
                self._add(l, value)
                l += 1
            if r & 1:
                # 左側の子
                r -= 1
                self._add(r, value)
            l >>= 1
            r >>= 1
        self._update(l0)
        self._update(r0 - 1)

    def get(self, l, r=None):
        """
        [l, r) の合計
        :param int l:
        :param int|None r:
        """
        if r is None:
            r = l + 1
        ret_l = []
        ret_r = []
        l += self._size
        r += self._size
        self._eval(l)
        self._eval(r - 1)
        while l < r:
            if l & 1:
                ret_l.append(self._tree[l])
                l += 1
            if r & 1:
                r -= 1
                ret_r.append(self._tree[r])
            l >>= 1
            r >>= 1
        return reduce(self._fn, ret_l + ret_r[::-1])


## ac-library
## 区間 max、区間 chmax
## https://atcoder.jp/contests/abc382/submissions/61522085
# op = max
# e = -1
# mapping = lambda f, s: max(f, s)
# composition = lambda f, g: max(f, g)
# id = -1
# values = [...]
# st = atcoder.lazysegtree.LazySegTree(op, e, mapping, composition, id, values)

## 区間 max、区間 update
## https://atcoder.jp/contests/abc382/submissions/61522219
# op = max
# e = -1
# mapping = lambda f, s: f if f >= 0 else s
# composition = lambda f, g: max(f, g)
# id = -1
# values = [...]
# st = atcoder.lazysegtree.LazySegTree(op, e, mapping, composition, id, values)


## 区間 min、区間 add
# op = min
# e = IINF
# mapping = add
# composition = add
# id = 0
# values = [...]
# st = atcoder.lazysegtree.LazySegTree(op, e, mapping, composition, id, values)


# ac-library
# atcoder.lazysegtree.LazySegTree(...)
# https://betrue12.hateblo.jp/entry/2020/09/23/005940


if __name__ == "__main__":
    st = SegmentTree([0] * 4, op=operator.add)
    st.add(1, 1)
    st.add(2, 2)
    st.add(3, 3)
    assert st.get(1, 3) == 3
    assert st.get(1, 4) == 6
    assert st.get(2, 4) == 5

    st = SegmentTree([2 ** 31 - 1] * 3, op=min)
    st.set(1, 5)
    assert st.get(0, 1) == 2 ** 31 - 1
    assert st.get(0, 2) == 5
    assert st.get(1, 3) == 5

    import numpy as np
    import itertools

    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9]

    # Test LazySegmentTreeAddMin
    st1 = LazySegmentTreeAddMin(values)
    test = np.array(values, dtype=int)
    i = 0
    for l, r in itertools.combinations_with_replacement(range(len(values)), r=2):
        r += 1
        if i % 3 == 0:
            assert st1.get(l, r) == test[l:r].min()
        st1.add(l, r, i * pow(-1, i))
        test[l: r] += i * pow(-1, i)
        i += 1

    # Test LazySegmentTreeAddSum
    st1 = LazySegmentTreeAddSum(values)
    test = np.array(values, dtype=int)
    i = 0
    for l, r in itertools.combinations_with_replacement(range(len(values)), r=2):
        r += 1
        if i % 3 == 0:
            assert st1.get(l, r) == test[l:r].sum()
        st1.add(l, r, i * pow(-1, i))
        test[l: r] += i * pow(-1, i)
        i += 1
