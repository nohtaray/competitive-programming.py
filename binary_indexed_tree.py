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
        :return:
        """
        x = i + 1
        while x <= self._size:
            self._bit[x - 1] += w
            x += x & -x

    def sum(self, i):
        """
        0 番目から i 番目までの合計
        :param int i:
        :return:
        """
        ret = 0
        x = i + 1
        while x > 0:
            ret += self._bit[x - 1]
            x -= x & -x
        return ret

    def __len__(self):
        return self._size


def compress(li):
    """
    大小関係を保ったまま 1 以上の数値に圧縮する。
    scipy.stats.rankdata に近い感じ
    :param list li:
    :rtype: list of int
    """
    ret = [0] * len(li)
    rank = 0
    prev = None
    for a, i in sorted([(a, i) for i, a in enumerate(li)]):
        if a != prev:
            rank += 1
        ret[i] = rank
    return ret


def count_inversions(li, max=None):
    """
    遅いので制限時間シビアなときは PyPy 推奨
    リストから転倒数 (li[i] > li[j] (i < j) となる (i, j) の組み合わせ数) を返す
    バブルソートするときに反転する必要がある数。
    :param numpy.ndarray | list of int li:
            すべての要素が 0 以上の int である配列。
            BIT を使うので、マイナスを含んだり最大値が大きい場合は↑の compress か
            np.argsort か scipy.stats.rankdata を使う。全部 O(logN) だとおもう
            リストに重複を含む場合は np.argsort は unstable なのでつかわない。
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


if __name__ == "__main__":
    # https://atcoder.jp/contests/chokudai_s001/tasks/chokudai_S001_j
    _ = int(input())
    li = list(map(int, input().split()))
    print(count_inversions(li, max=100000))
