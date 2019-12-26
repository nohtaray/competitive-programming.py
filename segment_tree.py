import operator
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

    def __len__(self):
        return self._size


class LazySegmentTree:
    # http://tsutaj.hatenablog.com/entry/2017/03/29/204841
    def __init__(self, size, fn=operator.add, default=None, initial_values=None):
        """
        :param int size:
        :param callable fn: 区間に適用する関数。引数を 2 つ取る。min, max, operator.xor など
        :param default:
        :param list initial_values:
        """
        default = default or 0

        # size 以上である最小の 2 冪を size とする
        self._size = 1 << (size - 1).bit_length()
        self._fn = fn

        self._lazy = [0] * (self._size * 2 - 1)
        self._tree = [default] * (self._size * 2 - 1)
        if initial_values:
            i = self._size - 1
            for v in initial_values:
                self._tree[i] = v
                i += 1
            i = self._size - 2
            while i >= 0:
                self._tree[i] = self._fn(self._tree[i * 2 + 1], self._tree[i * 2 + 2])
                i -= 1

    def add(self, from_i, to_i, value, k=0, L=None, r=None):
        """
        [from_i, to_i) を、それぞれの値と value に fn を適用した値で更新する
        :param int from_i:
        :param int to_i:
        :param int value:
        :param int k: self._tree のインデックス
        :param int L:
        :param int r:
        :return:
        """
        L = 0 if L is None else L
        r = self._size if r is None else r

        self._eval(k, L, r)

        # 範囲外
        if to_i <= L or r <= from_i:
            return

        if from_i <= L and r <= to_i:
            # 完全に被覆してる
            self._lazy[k] += (r - L) * value
            self._eval(k, L, r)
        else:
            # 中途半端
            self.add(from_i, to_i, value, k * 2 + 1, L, (L + r) // 2)
            self.add(from_i, to_i, value, k * 2 + 2, (L + r) // 2, r)
            self._tree[k] = self._fn(self._tree[k * 2 + 1], self._tree[k * 2 + 2])

    def _eval(self, k, L, r):
        """
        遅延配列の値を評価する
        :param k:
        :param L:
        :param r:
        """
        if self._lazy[k] != 0:
            # 本体を更新
            self._tree[k] += self._lazy[k]
            # 一番下じゃなければ伝播させる
            if r - L > 1:
                self._lazy[k * 2 + 1] += self._lazy[k] >> 1
                self._lazy[k * 2 + 2] += self._lazy[k] >> 1
            self._lazy[k] = 0

    def get(self, from_i, to_i, k=0, L=None, r=None):
        """
        [from_i, to_i) に fn を適用した結果を返す
        :param int from_i:
        :param int to_i:
        :param int k: self._tree[k] が、[L, r) に fn を適用した結果を持つ
        :param int L:
        :param int r:
        :return:
        """
        L = 0 if L is None else L
        r = self._size if r is None else r

        self._eval(k, L, r)

        if from_i <= L and r <= to_i:
            return self._tree[k]

        if to_i <= L or r <= from_i:
            return None

        ret_L = self.get(from_i, to_i, k * 2 + 1, L, (L + r) // 2)
        ret_r = self.get(from_i, to_i, k * 2 + 2, (L + r) // 2, r)
        if ret_L is None:
            return ret_r
        if ret_r is None:
            return ret_L
        return self._fn(ret_L, ret_r)

    def __len__(self):
        return self._size


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
