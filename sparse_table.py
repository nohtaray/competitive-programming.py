import math


class SparseTable:
    """
    構築 O(NlogN)、クエリ O(1)
    """

    def __init__(self, values, fn):
        """
        :param list values:
        :param callable fn: 結合則を満たす冪等な関数。min、max など。add はだめ
        """
        self._values = values
        self._fn = fn

        # SparseTable を構築
        # self._table[i][p]: [i, i+2^p) に fn を適用した結果の値のインデックス
        self._table = self._build(values, fn)

        # self._msb[i]: 最上位ビット; どの p を見るべきか
        self._msb = [0] * (len(values) + 1)
        for i in range(2, len(values) + 1):
            self._msb[i] = self._msb[i >> 1] + 1

    @staticmethod
    def _build(values, fn):
        # AtCoder の PyPy 2.4.0 では math.log2 が使えない
        size = int(math.log(len(values), 2)) + 1

        st = [[0] * size for _ in range(len(values))]
        for i in range(len(values)):
            st[i][0] = i
        for p in range(1, size):
            for i in range(len(values)):
                q = min(i + (1 << (p - 1)), len(values) - 1)
                l = st[i][p - 1]
                r = st[q][p - 1]
                if values[l] == fn(values[l], values[r]):
                    st[i][p] = l
                else:
                    st[i][p] = r
        return st

    def get(self, a, b):
        """
        半開区間 [a, b) に fn を適用した結果
        :param int a:
        :param int b:
        """
        if b <= a:
            return None
        p = self._msb[b - a]
        return self._fn(
            self._values[self._table[a][p]], self._values[self._table[b - (1 << p)][p]]
        )
