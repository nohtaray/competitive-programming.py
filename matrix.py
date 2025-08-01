from libs import fft


def dump_matrix_bit(mat, width):
    """
    F2 体の行列を表示する
    :param list of int mat:
    :param int width:
    """
    import numpy as np

    for row in mat:
        print(np.binary_repr(row, width=width))


def poly_matrix_mul(m1, m2, mod, max_deg=None):
    """
    要素が多項式である行列の積
    """
    return fft.poly_matrix_mul(m1, m2, mod, max_deg)


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


def matrix_power_mod(matrix, n, mod):
    """
    numpy.linalg.matrix_power と一緒
    :param list of list matrix:
    :param int n:
    :param int mod:
    :rtype: list of list
    """
    assert n >= 0
    if n == 0:
        id_mat = [[0] * len(matrix) for _ in range(len(matrix))]
        for i in range(len(matrix)):
            id_mat[i][i] = 1
        return id_mat

    n -= 1
    ret = matrix  # 必要ならコピーする
    while n > 0:
        if n & 1:
            ret = matrix_mul_mod(ret, matrix, mod)
        matrix = matrix_mul_mod(matrix, matrix, mod)
        n >>= 1
    return ret


def matrix_mul_bit(rows, rhs):
    """
    行列とベクトルの積 (mod2)
    :param list of int rows: rows[i] は i 行目のビット列
    :param int rhs: 右辺のベクトルをビット列にしたもの (上位ビットが上)
    """
    ret = 0
    for row in rows:
        ret <<= 1
        ret |= (row & rhs).bit_count() & 1
    return ret


def gauss_jordan_bit(rows, n_cols, n_rhs=0):
    """
    掃き出し法で標準形にする
    O(HW^2)
    :param list of int rows: rows[i] は i 行目のビット列
    :param int n_cols: 拡大行列全体の列数 (ビット列の長さ)
    :param int n_rhs: 拡大部分の列数 (連立方程式なら 1, 逆行列計算なら n_cols/2)
    """
    rows = rows[:]
    n_rows = len(rows)
    rank = 0
    for w in reversed(range(n_rhs, n_cols)):
        if rank >= n_rows:
            break
        col = [a >> w & 1 for a in rows]
        if not any(col[rank:]):
            continue
        h = col.index(1, rank)
        pivot = rows[h]
        for i in range(n_rows):
            if col[i]:
                rows[i] ^= pivot
        rows[h] = rows[rank]
        rows[rank] = pivot
        rank += 1
    return rows, rank


def count_solutions_bit(rows, rhs, W, mod):
    """
    解の個数を求める
    O(HW^2)
    :param list of int rows: rows[i] は i 行目のビット列
    :param list of int rhs: rhs[i] は i 行目の右辺 (1 or 0)
    :param int W: rows のビット列の長さ (rhs は含まない)
    """
    H = len(rows)
    mat = [(a << 1) | b for a, b in zip(rows, rhs)]
    mat, rank = gauss_jordan_bit(mat, W + 1, 1)
    if rank < H and any(mat[rank:]):
        # 解無し
        return 0
    # 2^自由度
    free = W - rank
    return pow(2, free, mod)


def count_solutions_bit2(cols, rhs_bit, H, mod):
    """
    解の個数を求める
    https://trap.jp/post/435/
    O(WH^2)
    :param list of int cols: cols[i] は i 列目のビット列
    :param int rhs_bit: 右辺のベクトルをビット列にしたもの (ビット列の向きを cols と合わせること)
    :param int H: ビット列の長さ
    """
    # 横に倒して処理する
    W = H
    H = len(cols)
    A = cols
    mat, rank = gauss_jordan_bit(A, W)
    X = rhs_bit
    h = 0
    i = W
    while h < H and i >= 0 and X:
        while i and X and ~X >> i & 1:
            i -= 1
        if i < 0:
            break
        if mat[h] >> i & 1:
            X ^= mat[h]
            i -= 1
        h += 1
    # rhs_bit を作れないなら解の個数は 0、作れるなら 0 の行の数だけ自由度がある
    free = H - rank
    return pow(2, free, mod) if X == 0 else 0


def invert_matrix_bit(rows: list[int]) -> list[int] | None:
    """
    F2 体でビット列表現された行列 rows の逆行列を求める。
    rows を拡大係数行列 [rows | I] にし、掃き出し法を用いて rows^-1 を得る。

    :param rows: rows[i] は i 行目のビット列（長さ W の行列）
    :return: 逆行列（各行がビット列）または None（逆行列が存在しない場合）
    """
    H = W = len(rows)

    # 単位行列 I を右に拡張して [rows | I] を構築
    mat = [row << W | (1 << (W - i - 1)) for i, row in enumerate(rows)]

    # 拡張部分は W 列
    mat, rank = gauss_jordan_bit(mat, W * 2, W)

    if rank < W:
        return None  # 非正則、逆行列は存在しない

    # 各行の下位 W ビットが逆行列
    inverse = [row & ((1 << W) - 1) for row in mat]
    return inverse


def gauss_jordan_bool(mat, n_cols, n_rhs=0):
    """
    掃き出し法で標準形にする
    O(HW^2)
    :param list of (list of bool) mat:
    :param int n_cols: 拡大行列全体の列数 (ビット列の長さ)
    :param int n_rhs: 拡大部分の列数 (連立方程式なら 1, 逆行列計算なら n_cols/2)
    """
    mat = [row[:] for row in mat]
    H = len(mat)
    rank = 0
    for w in range(n_cols - n_rhs):
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
    mat, rank = gauss_jordan_bool(mat, W + 1, 1)
    if rank < H and any([row[-1] for row in mat[rank:]]):
        # 解無し
        return 0
    # 2^自由度
    free = W - rank
    return pow(2, free, mod)
