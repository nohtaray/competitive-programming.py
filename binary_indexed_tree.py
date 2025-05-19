class BinaryIndexedTree:
    # http://hos.ac/slides/20140319_bit.pdf
    def __init__(self, size):
        """
        :param int size:
        """
        self._bit = [0] * size
        self._size = size

    def add(self, i, w):
        """
        i 番目に w を加える
        :param int i:
        :param int w:
        """
        x = i + 1
        while x <= self._size:
            self._bit[x - 1] += w
            x += x & -x

    def get(self, i):
        return self.sum(i + 1) - self.sum(i)

    def set(self, i, v):
        self.add(self.sum(i - 1) - self.sum(i) + v)

    def sum(self, i):
        """
        [0, i) の合計
        :param int i:
        """
        if i <= 0:
            return 0
        ret = 0
        while i > 0:
            ret += self._bit[i - 1]
            i -= i & -i
        return ret

    def lower_bound(self, w):
        """
        合計が w 以上となるインデックス
        add に渡したときに w 以上の値が返ってくる最小の値 - 1
        bit.sum(x + 1) = a_0 + a_1 + a_2 + ... + a_x >= w となる x
        ※マイナスの要素がないこと
        w <= bit[0] のとき、0
        w == bit.sum(len(bit)) のとき、len(bit) - 1
        w > bit.sum(len(bit)) のとき、len(bit)
        https://algo-logic.info/binary-indexed-tree/
        :param w:
        """
        if w <= 0:
            return 0
        x = 0
        length = 1
        while length < self._size:
            length <<= 1
        while length > 0:
            if x + length - 1 < self._size and self._bit[x + length - 1] < w:
                w -= self._bit[x + length - 1]
                x += length
            length >>= 1
        return x

    def __len__(self):
        return self._size


class BinaryIndexedTree2D:
    # http://hos.ac/slides/20140319_bit.pdf
    def __init__(self, H, W):
        """
        :param int H:
        :param int W:
        """
        self._bit = [[0] * (W + 1) for _ in range(H + 1)]
        self._H = H
        self._W = W

    def add(self, h, w, a):
        """
        (h, w) に a を加える
        :param int h:
        :param int w:
        :param int a:
        """
        i = h + 1
        while i <= self._H:
            j = w + 1
            while j <= self._W:
                self._bit[i][j] += a
                j += j & -j
            i += i & -i

    def get(self, h, w):
        return (
            self.sum(h + 1, w + 1)
            - self.sum(h + 1, w)
            - self.sum(h, w + 1)
            + self.sum(h, w)
        )

    def set(self, h, w, a):
        self.add(h, w, a - self.get(h, w))

    def sum(self, h, w):
        """
        \sum_{i=0}^{h-1} \sum_{j=0}^{w-1} a_{i,j}
        :param int h:
        :param int w:
        """
        if h <= 0 or w <= 0:
            return 0
        ret = 0
        i = h
        while i > 0:
            j = w
            while j > 0:
                ret += self._bit[i][j]
                j -= j & -j
            i -= i & -i
        return ret


def compress(li, origin=0):
    """
    座圧
    :param li:
    :param int origin:
    """
    (*ret,) = map(
        {v: i + origin for i, v in enumerate(sorted(set(li)))}.__getitem__, li
    )
    v2i = {v: i for v, i in zip(li, ret)}
    if origin <= 1:
        i2v = [None] * (len(v2i) + origin)
        for v, i in v2i.items():
            i2v[i] = v
    else:
        i2v = {i: v for v, i in v2i.items()}
    return ret, v2i, i2v


def count_inversions(li, compress_values=False):
    """
    リストから転倒数 (li[i] > li[w] (i < w) となる (i, w) の組み合わせ数) を返す
    バブルソートするときに反転する必要がある数。
    :rtype: int
    """
    if compress_values:
        *li, _ = map({v: i for i, v in enumerate(sorted(set(li)))}.__getitem__, li)
    bit = BinaryIndexedTree(size=max(li) + 1)
    ret = 0
    for i in range(len(li)):
        ret += i - bit.sum(li[i] + 1)
        bit.add(li[i], 1)
    return ret


class OrderedSet:
    # sortedcontainers か、これ↓を使う
    # https://github.com/tatyam-prime/SortedSet
    pass
