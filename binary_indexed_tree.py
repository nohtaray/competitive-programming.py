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

    def sum(self, i):
        """
        [0, i) の合計
        :param int i:
        """
        ret = 0
        while i > 0:
            ret += self._bit[i - 1]
            i -= i & -i
        return ret

    def __len__(self):
        return self._size


def compress(li, origin=0):
    """
    座圧
    :param li:
    :param int origin:
    :rtype: list of int
    """
    *ret, = map({v: i + origin for i, v in enumerate(sorted(set(li)))}.__getitem__, li)
    return ret


def count_inversions(li, max=None):
    """
    リストから転倒数 (li[i] > li[w] (i < w) となる (i, w) の組み合わせ数) を返す
    バブルソートするときに反転する必要がある数。
    :param numpy.ndarray | list of int li:
            すべての要素が 0 以上の int である配列。
            BIT を使うので、マイナスを含んだり最大値が大きい場合は np.argsort の結果を指定
            ただしリストに重複を含む場合は np.argsort は unstable なので別の方法使うこと
            https://docs.scipy.org/doc/numpy/reference/generated/numpy.sort.html
    :param int max: li の最大値。わかる場合は指定
    :rtype: int
    """
    if not max:
        max = __builtins__.max(li)
    bit = BinaryIndexedTree(size=max + 1)
    ret = 0
    for i in range(len(li)):
        ret += i - bit.sum(li[i])
        bit.add(li[i], 1)
    return ret
