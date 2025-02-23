from functools import cmp_to_key


def area(x, y):
    """
    象限を返す
    原点は 0
    :param int x:
    :param int y:
    """
    return 0 if x == y == 0 else (3 if x < 0 else 4) if y < 0 else (2 if x < 0 else 1)


def polar_angle_sort_cmp(p, q):
    """
    偏角ソートの比較関数
    角度が同じ点同士は 0
    :param (int, int) p:
    :param (int, int) q:
    """
    px, py = p
    qx, qy = q
    ap = area(px, py)
    aq = area(qx, qy)
    # 象限で比較
    if ap != aq:
        return ap - aq
    # 外積で比較
    return py * qx - px * qy


def polar_angle_sort(points):
    """
    偏角ソート
    角度が同じ点同士の順序は入力のまま
    :param list of (int, int) points:
    """
    points.sort(key=cmp_to_key(polar_angle_sort_cmp))
