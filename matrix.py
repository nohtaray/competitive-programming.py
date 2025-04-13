import operator
from functools import reduce


def matrix_mul_mod(m1, m2, mod):
    """
    :param list of list m1:
    :param list of list m2:
    :param int mod:
    :rtype: list of list
    """
    rows = []
    for r1 in range(len(m1)):
        row = []
        for c2 in range(len(m2[0])):
            s = 0
            for r2 in range(len(m2)):
                s += m1[r1][r2] * m2[r2][c2] % mod
            row.append(s % mod)
        rows.append(row)
    return rows


def matrix_add_mod(m1, m2, mod):
    """
    :param list of list m1:
    :param list of list m2:
    :param int mod:
    :rtype: list of list
    """
    ret = []
    for i in range(len(m1)):
        row = []
        for j in range(len(m1[i])):
            row.append((m1[i][j] + m2[i][j]) % mod)
        ret.append(row)
    return ret


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


def gauss_jordan_bit(mat, W):
    """
    掃き出し法で標準形 (を左右反転したもの) にする
    O(HW^2)
    :param list of int mat: mat[i] は i 行目のビット列
    :param int W: ビット列の長さ; 連立方程式を解くときは解の存在判定ができるように -1 した値を渡すこと
    """
    mat = mat[:]
    H = len(mat)
    rank = 0
    for w in range(W):
        if rank >= H:
            break
        col = [row >> w & 1 for row in mat]
        if not any(col[rank:]):
            continue
        h = col.index(1, rank)
        pivot = mat[h]
        for i in range(H):
            if col[i]:
                mat[i] ^= pivot
        mat[h] = mat[rank]
        mat[rank] = pivot
        rank += 1
    return mat, rank


def count_solutions_bit(A, rhs, W, mod):
    """
    解の個数を求める
    O(HW^2)
    :param list of int A: A[i] は i 行目のビット列
    :param list of int rhs: rhs[i] は i 行目の右辺 (1 or 0)
    :param int W: A のビット列の長さ (rhs は含まない)
    """
    H = len(A)
    mat = [row | (b << W) for row, b in zip(A, rhs)]
    mat, rank = gauss_jordan_bit(mat, W)
    if rank < H and any(mat[rank:]):
        # 解無し
        return 0
    # 2^自由度
    free = W - rank
    return pow(2, free, mod)


def gauss_jordan_bool(mat, W):
    """
    掃き出し法で標準形にする
    O(HW^2)
    :param list of (list of bool) mat:
    :param int W: 処理する列数; 連立方程式を解くときは解の存在判定ができるように mat の列数から -1 した値を渡すこと
    """
    mat = [row[:] for row in mat]
    H = len(mat)
    rank = 0
    for w in range(W):
        if rank >= H:
            break
        col = [row[w] for row in mat]
        if not any(col[rank:]):
            continue
        h = col.index(True, rank)
        pivot = mat[h]
        for i in range(H):
            if i != h and col[i]:
                for w in range(len(pivot)):
                    mat[i][w] ^= pivot[w]
        mat[h], mat[rank] = mat[rank], mat[h]
        rank += 1
    return mat, rank


def count_solutions_bool(A, rhs, mod):
    """
    解の個数を求める
    O(HW^2)
    :param list of (list of bool) A:
    :param list of bool rhs: rhs[i] は i 行目の右辺 (1 or 0)
    """
    H = len(A)
    W = len(A[0])
    mat = [[*a, b] for a, b in zip(A, rhs)]
    mat, rank = gauss_jordan_bool(mat, W)
    if rank < H and any([row[-1] for row in mat[rank:]]):
        # 解無し
        return 0
    # 2^自由度
    free = W - rank
    return pow(2, free, mod)
