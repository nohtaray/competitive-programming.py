import cmath
import math
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


class PointInt:
    """
    2次元空間上の点
    """

    # 反時計回り側にある
    CCW_COUNTER_CLOCKWISE = 1
    # 時計回り側にある
    CCW_CLOCKWISE = -1
    # 線分の後ろにある
    CCW_ONLINE_BACK = 2
    # 線分の前にある
    CCW_ONLINE_FRONT = -2
    # 線分上にある
    CCW_ON_SEGMENT = 0

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, p):
        """
        :param PointInt p:
        """
        return PointInt(self.x + p.x, self.y + p.y)

    def __iadd__(self, p):
        """
        :param PointInt p:
        """
        self.x += p.x
        self.y += p.y
        return self

    def __sub__(self, p):
        """
        :param PointInt p:
        """
        return PointInt(self.x - p.x, self.y - p.y)

    def __isub__(self, p):
        """
        :param PointInt p:
        """
        self.x -= p.x
        self.y -= p.y
        return self

    def __mul__(self, f: int):
        return PointInt(self.x * f, self.y * f)

    def __imul__(self, f: int):
        self.x *= f
        self.y *= f
        return self

    def __truediv__(self, f: int):
        raise NotImplementedError

    def __itruediv__(self, f: int):
        raise NotImplementedError

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __neg__(self):
        return PointInt(-self.x, -self.y)

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __abs__(self):
        return math.hypot(self.x, self.y)

    # sort() に渡せるように適当に順序付けておく。x の小さい順、x が同じなら y の小さい順。
    def __lt__(self, p):
        return self.x - p.x <= 0 and self.y - p.y < 0

    def __le__(self, p):
        return self.x - p.x <= 0 and self.y - p.y <= 0

    def __gt__(self, p):
        return self.x - p.x >= 0 and self.y - p.y > 0

    def __ge__(self, p):
        return self.x - p.x >= 0 and self.y - p.y >= 0

    @staticmethod
    def ccw(a, b, c):
        """
        線分 ab に対する c の位置
        線分上にあるか判定するだけなら on_segment とかのが速い
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_C&lang=ja
        :param PointInt a:
        :param PointInt b:
        :param PointInt c:
        """
        b = b - a
        c = c - a
        det = b.det(c)
        if det > 0:
            return PointInt.CCW_COUNTER_CLOCKWISE
        if det < 0:
            return PointInt.CCW_CLOCKWISE
        if b.dot(c) < 0:
            return PointInt.CCW_ONLINE_BACK
        if b.dot(b - c) < 0:
            return PointInt.CCW_ONLINE_FRONT
        return PointInt.CCW_ON_SEGMENT

    def dot(self, p):
        """
        内積
        :param PointInt p:
        :rtype: float
        """
        return self.x * p.x + self.y * p.y

    def det(self, p):
        """
        外積
        :param PointInt p:
        :rtype: float
        """
        return self.x * p.y - self.y * p.x

    def dist(self, p):
        """
        距離
        float で返すので丸めが怖いときは sqr_dist を使うこと
        :param PointInt p:
        :rtype: float
        """
        return abs(self - p)

    def sqr_dist(self, p):
        """
        距離の二乗
        :param PointInt p:
        :rtype: int
        """
        return (self.x - p.x) ** 2 + (self.y - p.y) ** 2

    def norm(self):
        """
        原点からの距離
        :rtype: float
        """
        return abs(self)

    def sqr_norm(self):
        """
        原点からの距離の二乗
        :rtype: int
        """
        return self.x ** 2 + self.y ** 2

    def phase(self):
        """
        原点からの角度
        :rtype: float
        """
        return cmath.phase(self.x + self.y * 1j)

    def angle(self, p, q):
        """
        p に向いてる状態から q まで反時計回りに回転するときの角度
        -pi <= ret <= pi
        :param PointInt p:
        :param PointInt q:
        :rtype: float
        """
        return ((q - self).phase() - (p - self).phase() + cmath.pi) % cmath.tau - cmath.pi

    def area2(self, p, q):
        """
        p, q となす三角形の面積を 2 倍した値 (int)
        外側で割るときは丸めに注意
        :param PointInt p:
        :param PointInt q:
        :rtype: int
        """
        return abs((p - self).det(q - self))

    def rotate(self, theta):
        """
        反時計回りに theta だけ回転させた Point を返す
        :param float theta:
        """
        raise NotImplementedError
        # c = self.c * cmath.rect(1, theta)
        # return Point(c.real, c.imag)

    def projection_point(self, p, q, allow_outer=False):
        """
        線分 pq を通る直線上に垂線をおろしたときの足の座標
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_A&lang=ja
        :param PointInt p:
        :param PointInt q:
        :param allow_outer: 答えが線分の間になくても OK
        :rtype: PointInt|None
        """
        raise NotImplementedError
        # diff_q = q - p
        # # 答えの p からの距離
        # r = (self - p).dot(diff_q) / abs(diff_q)
        # # 線分の角度
        # phase = diff_q.phase()
        #
        # ret = PointInt.from_polar(r, phase) + p
        # if allow_outer or (p - ret).dot(q - ret) < EPS:
        #     return ret
        # return None

    def reflection_point(self, p, q):
        """
        直線 pq を挟んで反対にある点
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_B&lang=ja
        :param PointInt p:
        :param PointInt q:
        :rtype: PointInt
        """
        raise NotImplementedError
        # # 距離
        # r = abs(self - p)
        # # pq と p-self の角度
        # angle = p.angle(q, self)
        # # 直線を挟んで角度を反対にする
        # angle = (q - p).phase() - angle
        # return PointInt.from_polar(r, angle) + p

    def on_segment(self, p, q, allow_side=True):
        """
        点が線分 pq の上に乗っているか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_C&lang=ja
        :param PointInt p:
        :param PointInt q:
        :param allow_side: 端っこでギリギリ触れているのを許容するか
        :rtype: bool
        """
        if not allow_side and (self == p or self == q):
            return False
        # 外積がゼロ: 面積がゼロ == 一直線
        # 内積がマイナス: p - self - q の順に並んでる
        return abs((p - self).det(q - self)) == 0 and (p - self).dot(q - self) <= 0

    @staticmethod
    def circumcenter_of(p1, p2, p3):
        """
        外心
        :param PointInt p1:
        :param PointInt p2:
        :param PointInt p3:
        :rtype: PointInt|None
        """
        if abs((p2 - p1).det(p3 - p1)) == 0:
            # 外積がゼロ == 一直線
            return None
        # https://ja.wikipedia.org/wiki/外接円
        a = (p2.x - p3.x) ** 2 + (p2.y - p3.y) ** 2
        b = (p3.x - p1.x) ** 2 + (p3.y - p1.y) ** 2
        c = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
        num = p1 * a * (b + c - a) + p2 * b * (c + a - b) + p3 * c * (a + b - c)
        den = a * (b + c - a) + b * (c + a - b) + c * (a + b - c)
        return num / den

    @staticmethod
    def incenter_of(p1, p2, p3):
        """
        内心
        :param PointInt p1:
        :param PointInt p2:
        :param PointInt p3:
        """
        raise NotImplementedError
        # # https://ja.wikipedia.org/wiki/三角形の内接円と傍接円
        # d1 = p2.dist(p3)
        # d2 = p3.dist(p1)
        # d3 = p1.dist(p2)
        # return (p1 * d1 + p2 * d2 + p3 * d3) / (d1 + d2 + d3)


class PolygonInt:
    """
    2次元空間上の多角形
    """

    def __init__(self, points):
        """
        :param list of PointInt points:
        """
        self.points = points

    def iter2(self):
        """
        隣り合う2点を順に返すイテレータ
        :rtype: typing.Iterator[(PointInt, PointInt)]
        """
        return zip(self.points, self.points[1:] + self.points[:1])

    def iter3(self):
        """
        隣り合う3点を順に返すイテレータ
        :rtype: typing.Iterator[(PointInt, PointInt, PointInt)]
        """
        return zip(self.points,
                   self.points[1:] + self.points[:1],
                   self.points[2:] + self.points[:2])

    def area2(self):
        """
        面積を 2 倍した値 (int)
        外側で割るときは丸めに注意
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_3_A&lang=ja
        """
        # 外積の和 / 2
        dets = []
        for p, q in self.iter2():
            dets.append(p.det(q))
        return abs(sum(dets))

    def is_convex(self, allow_straight=False, allow_collapsed=False):
        """
        凸多角形かどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_3_B&lang=ja
        :param allow_straight: 3点がまっすぐ並んでるのを許容するかどうか
        :param allow_collapsed: 面積がゼロの場合を許容するか
        """
        ccw = []
        for a, b, c in self.iter3():
            ccw.append(PointInt.ccw(a, b, c))
        ccw = set(ccw)
        if len(ccw) == 1:
            if ccw == {PointInt.CCW_CLOCKWISE}:
                return True
            if ccw == {PointInt.CCW_COUNTER_CLOCKWISE}:
                return True
        if allow_straight and len(ccw) == 2:
            if ccw == {PointInt.CCW_ONLINE_FRONT, PointInt.CCW_CLOCKWISE}:
                return True
            if ccw == {PointInt.CCW_ONLINE_FRONT, PointInt.CCW_COUNTER_CLOCKWISE}:
                return True
        if allow_collapsed and len(ccw) == 3:
            return ccw == {PointInt.CCW_ONLINE_FRONT, PointInt.CCW_ONLINE_BACK, PointInt.CCW_ON_SEGMENT}
        return False

    def has_point_on_edge(self, p):
        """
        指定した点が辺上にあるか
        :param PointInt p:
        :rtype: bool
        """
        for a, b in self.iter2():
            if p.on_segment(a, b):
                return True
        return False

    def contains(self, p, allow_on_edge=True):
        """
        指定した点を含むか
        Winding Number Algorithm
        https://www.nttpc.co.jp/technology/number_algorithm.html
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_3_C&lang=ja
        :param PointInt p:
        :param bool allow_on_edge: 辺上の点を許容するか
        """
        raise NotImplementedError
        # angles = []
        # for a, b in self.iter2():
        #     if p.on_segment(a, b):
        #         return allow_on_edge
        #     angles.append(p.angle(a, b))
        # # 一周以上するなら含む
        # return abs(math.fsum(angles)) > EPS

    @staticmethod
    def convex_hull(points, allow_straight=False):
        """
        凸包。x が最も小さい点のうち y が最も小さい点から反時計回り。
        Graham Scan O(N log N)
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_4_A&lang=ja
        :param list of PointInt points:
        :param allow_straight: 3点がまっすぐ並んでるのを許容するかどうか
        :rtype: list of PointInt
        """
        points = points[:]
        points.sort(key=lambda p: (p.x, p.y))

        # allow_straight なら 0 を許容する
        det_lower = 0 if allow_straight else 1

        sz = 0
        #: :type: list of (PointInt|None)
        ret = [None] * (len(points) * 2)
        for p in points:
            while sz > 1 and (ret[sz - 1] - ret[sz - 2]).det(p - ret[sz - 1]) < det_lower:
                sz -= 1
            ret[sz] = p
            sz += 1
        floor = sz
        for p in reversed(points[:-1]):
            while sz > floor and (ret[sz - 1] - ret[sz - 2]).det(p - ret[sz - 1]) < det_lower:
                sz -= 1
            ret[sz] = p
            sz += 1
        ret = ret[:sz - 1]

        if allow_straight and len(ret) > len(points):
            # allow_straight かつ全部一直線のときに二重にカウントしちゃう
            ret = points
        return ret

    @staticmethod
    def sqr_diameter(points):
        """
        直径の二乗
        凸包構築 O(N log N) + カリパー法 O(N)
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_4_B&lang=ja
        :param list of PointInt points:
        """
        # 反時計回り
        points = PolygonInt.convex_hull(points, allow_straight=False)
        if len(points) == 1:
            return 0
        if len(points) == 2:
            return (points[0] - points[1]).sqr_norm()

        # x軸方向に最も遠い点対
        si = points.index(min(points, key=lambda p: (p.x, p.y)))
        sj = points.index(max(points, key=lambda p: (p.x, p.y)))
        n = len(points)

        ret = 0
        # 半周回転
        i, j = si, sj
        while i != sj or j != si:
            ret = max(ret, (points[i] - points[j]).sqr_norm())
            ni = (i + 1) % n
            nj = (j + 1) % n
            # 2つの辺が並行になる方向にずらす
            if (points[ni] - points[i]).det(points[nj] - points[j]) > 0:
                j = nj
            else:
                i = ni
        return ret
