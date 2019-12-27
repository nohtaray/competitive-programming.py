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
