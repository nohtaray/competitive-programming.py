import operator
from functools import reduce


def matrix_mul(m1, m2):
    """
    np.dot(m1, m2) と一緒
    :param list of list m1:
    :param list of list m2:
    :rtype: list of list
    """
    rows = []
    for r1 in range(len(m1)):
        row = []
        for c2 in range(len(m2[0])):
            row.append(reduce(operator.add, [m1[r1][r2] * m2[r2][c2] for r2 in range(len(m2))]))
        rows.append(row)
    return rows


def matrix_power(matrix, n, id_mat=None):
    """
    numpy.linalg.matrix_power と一緒
    :param list of list matrix:
    :param int n:
    :param list of list id_mat: 単位行列
    :rtype: list of list
    """
    assert n >= 0
    if n == 0:
        return id_mat

    n -= 1
    ret = matrix  # 必要ならコピーする
    while n > 0:
        if n & 1:
            ret = matrix_mul(ret, matrix)
        matrix = matrix_mul(matrix, matrix)
        n >>= 1
    return ret
