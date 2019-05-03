import operator


class SegmentTree:
    # http://tsutaj.hatenablog.com/entry/2017/03/29/204841
    def __init__(self, size, fn=operator.add, default=0):
        """
        :param int size:
        :param callable fn: 区間に適用する関数。引数を 2 つ取る。min, max, operator.xor など
        """
        # size 以上である最小の 2 冪
        n = 1
        while n < size:
            n *= 2
        self._size = n
        self._tree = [default for _ in range(self._size * 2 - 1)]
        self._fn = fn

    def set(self, i, value):
        """
        i 番目に value を設定
        :param int i:
        :param int value:
        :return:
        """
        x = self._size - 1 + i
        self._tree[x] = value

        while x > 0:
            x = (x - 1) // 2
            self._tree[x] = self._fn(self._tree[x * 2 + 1], self._tree[x * 2 + 2])

    def add(self, i, value):
        """
        もとの i 番目と value に fn を適用したものを i 番目に設定
        :param int i:
        :param int value:
        :return:
        """
        x = self._size - 1 + i
        self.set(i, self._fn(self._tree[x], value))

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


if __name__ == '__main__':
    st = SegmentTree(size=4, fn=operator.add, default=0)
    st.add(1, 1)
    st.add(2, 2)
    st.add(3, 3)
    assert st.get(1, 3) == 3
    assert st.get(1, 4) == 6
    assert st.get(2, 4) == 5

    st = SegmentTree(size=3, fn=min, default=2 ** 31 - 1)
    st.set(1, 5)
    assert st.get(0, 1) == 2 ** 31 - 1
    assert st.get(0, 2) == 5
    assert st.get(1, 3) == 5
