import operator
from functools import reduce


def matrix_mul(m1, m2):
    """
    np.dot(m1, m2) と一緒
    :param list of list m1:
    :param list of list m2:
    :return:
    """
    rows = []
    for r1 in range(len(m1)):
        row = []
        for c2 in range(len(m2[0])):
            row.append(reduce(operator.xor, [m1[r1][r2] & m2[r2][c2] for r2 in range(len(m2))]))
        rows.append(row)
    return rows


def matrix_power(matrix, n):
    """
    numpy.linalg.matrix_power と一緒
    :param list of list matrix:
    :param int n:
    :return:
    """
    eye = []
    for i in range(len(matrix)):
        row = [0] * len(matrix)
        row[i] = 2 ** 32 - 1
        eye.append(row)

    ret = eye
    while n > 0:
        if n & 1:
            ret = matrix_mul(ret, matrix)
        matrix = matrix_mul(matrix, matrix)
        n >>= 1
    return ret
