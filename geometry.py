import cmath
import itertools
import math
import random
from collections import defaultdict

INF = float("inf")
PI = cmath.pi
TAU = cmath.pi * 2
EPS = 1e-10


class Point:
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

    def __init__(self, x: float, y: float):
        self.c = complex(x, y)

    @property
    def x(self):
        return self.c.real

    @property
    def y(self):
        return self.c.imag

    @staticmethod
    def from_complex(c: complex):
        return Point(c.real, c.imag)

    @staticmethod
    def from_polar(r: float, phi: float):
        c = cmath.rect(r, phi)
        return Point(c.real, c.imag)

    def __add__(self, p):
        """
        :param Point p:
        """
        c = self.c + p.c
        return Point(c.real, c.imag)

    def __iadd__(self, p):
        """
        :param Point p:
        """
        self.c += p.c
        return self

    def __sub__(self, p):
        """
        :param Point p:
        """
        c = self.c - p.c
        return Point(c.real, c.imag)

    def __isub__(self, p):
        """
        :param Point p:
        """
        self.c -= p.c
        return self

    def __mul__(self, f: float):
        c = self.c * f
        return Point(c.real, c.imag)

    def __imul__(self, f: float):
        self.c *= f
        return self

    def __truediv__(self, f: float):
        c = self.c / f
        return Point(c.real, c.imag)

    def __itruediv__(self, f: float):
        self.c /= f
        return self

    def __repr__(self):
        return "({}, {})".format(round(self.x, 10), round(self.y, 10))

    def __neg__(self):
        c = -self.c
        return Point(c.real, c.imag)

    def __eq__(self, p):
        return abs(self.c - p.c) < EPS

    def __abs__(self):
        return abs(self.c)

    @staticmethod
    def ccw(a, b, c):
        """
        線分 ab に対する c の位置
        線分上にあるか判定するだけなら on_segment とかのが速い
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_C&lang=ja
        :param Point a:
        :param Point b:
        :param Point c:
        """
        b = b - a
        c = c - a
        det = b.det(c)
        if det > EPS:
            return Point.CCW_COUNTER_CLOCKWISE
        if det < -EPS:
            return Point.CCW_CLOCKWISE
        if b.dot(c) < -EPS:
            return Point.CCW_ONLINE_BACK
        if c.norm() - b.norm() > EPS:
            return Point.CCW_ONLINE_FRONT
        return Point.CCW_ON_SEGMENT

    def dot(self, p):
        """
        内積
        :param Point p:
        :rtype: float
        """
        return self.x * p.x + self.y * p.y

    def det(self, p):
        """
        外積
        :param Point p:
        :rtype: float
        """
        return self.x * p.y - self.y * p.x

    def dist(self, p):
        """
        距離
        :param Point p:
        :rtype: float
        """
        return abs(self.c - p.c)

    def norm(self):
        """
        原点からの距離
        :rtype: float
        """
        return abs(self.c)

    def phase(self):
        """
        原点からの角度
        :rtype: float
        """
        return cmath.phase(self.c)

    def angle(self, p, q):
        """
        p に向いてる状態から q まで反時計回りに回転するときの角度
        -pi <= ret <= pi
        :param Point p:
        :param Point q:
        :rtype: float
        """
        return (cmath.phase(q.c - self.c) - cmath.phase(p.c - self.c) + PI) % TAU - PI

    def area(self, p, q):
        """
        p, q となす三角形の面積
        :param Point p:
        :param Point q:
        :rtype: float
        """
        return abs((p - self).det(q - self) / 2)

    def projection_point(self, p, q, allow_outer=False):
        """
        線分 pq を通る直線上に垂線をおろしたときの足の座標
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_A&lang=ja
        :param Point p:
        :param Point q:
        :param allow_outer: 答えが線分の間になくても OK
        :rtype: Point|None
        """
        diff_q = q - p
        # 答えの p からの距離
        r = (self - p).dot(diff_q) / abs(diff_q)
        # 線分の角度
        phase = diff_q.phase()

        ret = Point.from_polar(r, phase) + p
        if allow_outer or (p - ret).dot(q - ret) < EPS:
            return ret
        return None

    def reflection_point(self, p, q):
        """
        直線 pq を挟んで反対にある点
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_B&lang=ja
        :param Point p:
        :param Point q:
        :rtype: Point
        """
        # 距離
        r = abs(self - p)
        # pq と p-self の角度
        angle = p.angle(q, self)
        # 直線を挟んで角度を反対にする
        angle = (q - p).phase() - angle
        return Point.from_polar(r, angle) + p

    def on_segment(self, p, q, allow_side=True):
        """
        点が線分 pq の上に乗っているか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_1_C&lang=ja
        :param Point p:
        :param Point q:
        :param allow_side: 端っこでギリギリ触れているのを許容するか
        :rtype: bool
        """
        if not allow_side and (self == p or self == q):
            return False
        # 外積がゼロ: 面積がゼロ == 一直線
        # 内積がマイナス: p - self - q の順に並んでる
        return abs((p - self).det(q - self)) < EPS and (p - self).dot(q - self) < EPS

    @staticmethod
    def circumstance_of(p1, p2, p3):
        """
        外心
        :param Point p1:
        :param Point p2:
        :param Point p3:
        :rtype: Point|None
        """
        if abs((p2 - p1).det(p3 - p1)) < EPS:
            # 外積がゼロ == 一直線
            return None
        # https://ja.wikipedia.org/wiki/外接円
        a = (p2.x - p3.x) ** 2 + (p2.y - p3.y) ** 2
        b = (p3.x - p1.x) ** 2 + (p3.y - p1.y) ** 2
        c = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2
        num = p1 * a * (b + c - a) + p2 * b * (c + a - b) + p3 * c * (a + b - c)
        den = a * (b + c - a) + b * (c + a - b) + c * (a + b - c)
        return num / den


class Line:
    """
    2次元空間上の直線
    """

    def __init__(self, a: float, b: float, c: float):
        """
        直線 ax + by + c = 0
        """
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def from_gradient(grad: float, intercept: float):
        """
        直線 y = ax + b
        :param grad: 傾き
        :param intercept: 切片
        :return:
        """
        return Line(grad, -1, intercept)

    @staticmethod
    def from_segment(p1, p2):
        """
        :param Point p1:
        :param Point p2:
        """
        a = p2.y - p1.y
        b = p1.x - p2.x
        c = p2.y * (p2.x - p1.x) - p2.x * (p2.y - p1.y)
        return Line(a, b, c)

    @property
    def gradient(self):
        """
        傾き
        """
        return INF if self.b == 0 else -self.a / self.b

    @property
    def intercept(self):
        """
        切片
        """
        return INF if self.b == 0 else -self.c / self.b

    def is_parallel_to(self, l):
        """
        平行かどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_A&lang=ja
        :param Line l:
        """
        # 法線ベクトル同士の外積がゼロ
        return abs(Point(self.a, self.b).det(Point(l.a, l.b))) < EPS

    def is_orthogonal_to(self, l):
        """
        直行しているかどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_A&lang=ja
        :param Line l:
        """
        # 法線ベクトル同士の内積がゼロ
        return abs(Point(self.a, self.b).dot(Point(l.a, l.b))) < EPS

    def intersection_point(self, l):
        """
        交差する点
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_C&lang=ja
        :param Line l:
        :rtype: Point|None
        """
        a1, b1, c1 = self.a, self.b, self.c
        a2, b2, c2 = l.a, l.b, l.c
        det = a1 * b2 - a2 * b1
        if abs(det) < EPS:
            # 並行
            return None
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        return Point(x, y)

    def dist(self, p):
        """
        他の点との最短距離
        :param Point p:
        """
        raise NotImplementedError()

    def has_point(self, p):
        """
        p が直線上に乗っているかどうか
        :param Point p:
        """
        return abs(self.a * p.x + self.b * p.y + self.c) < EPS


class Segment:
    """
    2次元空間上の線分
    """

    def __init__(self, p1, p2):
        """
        :param Point p1:
        :param Point p2:
        """
        self.p1 = p1
        self.p2 = p2

    def norm(self):
        """
        線分の長さ
        """
        return abs(self.p1 - self.p2)

    def phase(self):
        """
        p1 を原点としたときの p2 の角度
        """
        return (self.p2 - self.p1).phase()

    def is_parallel_to(self, s):
        """
        平行かどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_A&lang=ja
        :param Segment s:
        :return:
        """
        # 外積がゼロ
        return abs((self.p1 - self.p2).det(s.p1 - s.p2)) < EPS

    def is_orthogonal_to(self, s):
        """
        直行しているかどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_A&lang=ja
        :param Segment s:
        :return:
        """
        # 内積がゼロ
        return abs((self.p1 - self.p2).dot(s.p1 - s.p2)) < EPS

    def intersects_with(self, s, allow_side=True):
        """
        交差するかどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_B&lang=ja
        :param Segment s:
        :param allow_side: 端っこでギリギリ触れているのを許容するか
        """
        if self.is_parallel_to(s):
            # 並行なら線分の端点がもう片方の線分の上にあるかどうか
            return (s.p1.on_segment(self.p1, self.p2, allow_side) or
                    s.p2.on_segment(self.p1, self.p2, allow_side) or
                    self.p1.on_segment(s.p1, s.p2, allow_side) or
                    self.p2.on_segment(s.p1, s.p2, allow_side))
        else:
            # allow_side ならゼロを許容する
            det_upper = EPS if allow_side else -EPS
            ok = True
            # self の両側に s.p1 と s.p2 があるか
            ok &= (self.p2 - self.p1).det(s.p1 - self.p1) * (self.p2 - self.p1).det(s.p2 - self.p1) < det_upper
            # s の両側に self.p1 と self.p2 があるか
            ok &= (s.p2 - s.p1).det(self.p1 - s.p1) * (s.p2 - s.p1).det(self.p2 - s.p1) < det_upper
            return ok

    def closest_point(self, p):
        """
        線分上の、p に最も近い点
        :param Point p:
        """
        # p からおろした垂線までの距離
        d = (p - self.p1).dot(self.p2 - self.p1) / self.norm()
        # p1 より前
        if d < EPS:
            return self.p1
        # p2 より後
        if -EPS < d - self.norm():
            return self.p2
        # 線分上
        return Point.from_polar(d, (self.p2 - self.p1).phase()) + self.p1

    def dist(self, p):
        """
        他の点との最短距離
        :param Point p:
        """
        return abs(p - self.closest_point(p))

    def dist_segment(self, s):
        """
        他の線分との最短距離
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_D&lang=ja
        :param Segment s:
        """
        if self.intersects_with(s):
            return 0.0
        return min(
            self.dist(s.p1),
            self.dist(s.p2),
            s.dist(self.p1),
            s.dist(self.p2),
        )

    def has_point(self, p, allow_side=True):
        """
        p が線分上に乗っているかどうか
        :param Point p:
        :param allow_side: 端っこでギリギリ触れているのを許容するか
        """
        return p.on_segment(self.p1, self.p2, allow_side=allow_side)


class Polygon:
    """
    2次元空間上の多角形
    """

    def __init__(self, points):
        """
        :param list of Point points:
        """
        self.points = points

    def iter2(self):
        """
        隣り合う2点を順に返すイテレータ
        :rtype: typing.Iterator[(Point, Point)]
        """
        return zip(self.points, self.points[1:] + self.points[:1])

    def iter3(self):
        """
        隣り合う3点を順に返すイテレータ
        :rtype: typing.Iterator[(Point, Point, Point)]
        """
        return zip(self.points,
                   self.points[1:] + self.points[:1],
                   self.points[2:] + self.points[:2])

    def area(self):
        """
        面積
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_3_A&lang=ja
        """
        # 外積の和 / 2
        dets = []
        for p, q in self.iter2():
            dets.append(p.det(q))
        return abs(math.fsum(dets)) / 2

    def is_convex(self, allow_straight=False, allow_collapsed=False):
        """
        凸多角形かどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_3_B&lang=ja
        :param allow_straight: 3点がまっすぐ並んでるのを許容するかどうか
        :param allow_collapsed: 面積がゼロの場合を許容するか
        """
        ccw = []
        for a, b, c in self.iter3():
            ccw.append(Point.ccw(a, b, c))
        ccw = set(ccw)
        if len(ccw) == 1:
            if ccw == {Point.CCW_CLOCKWISE}:
                return True
            if ccw == {Point.CCW_COUNTER_CLOCKWISE}:
                return True
        if allow_straight and len(ccw) == 2:
            if ccw == {Point.CCW_ONLINE_FRONT, Point.CCW_CLOCKWISE}:
                return True
            if ccw == {Point.CCW_ONLINE_FRONT, Point.CCW_COUNTER_CLOCKWISE}:
                return True
        if allow_collapsed and len(ccw) == 3:
            return ccw == {Point.CCW_ONLINE_FRONT, Point.CCW_ONLINE_BACK, Point.CCW_ON_SEGMENT}
        return False

    def has_point_on_edge(self, p):
        """
        指定した点が辺上にあるか
        :param Point p:
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
        :param Point p:
        :param bool allow_on_edge: 辺上の点を許容するか
        """
        angles = []
        for a, b in self.iter2():
            if p.on_segment(a, b):
                return allow_on_edge
            angles.append(p.angle(a, b))
        # 一周以上するなら含む
        return abs(math.fsum(angles)) > EPS

    @staticmethod
    def convex_hull(points, allow_straight=False):
        """
        凸包。x が最も小さい点のうち y が最も小さい点から反時計回り。
        Graham Scan O(N log N)
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_4_A&lang=ja
        :param list of Point points:
        :param allow_straight: 3点がまっすぐ並んでるのを許容するかどうか
        :rtype: list of Point
        """
        points = points[:]
        points.sort(key=lambda p: (p.x, p.y))

        # allow_straight なら 0 を許容する
        det_lower = -EPS if allow_straight else EPS

        sz = 0
        #: :type: list of (Point|None)
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
    def diameter(points):
        """
        直径
        凸包構築 O(N log N) + カリパー法 O(N)
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_4_B&lang=ja
        :param list of Point points:
        """
        # 反時計回り
        points = Polygon.convex_hull(points, allow_straight=False)
        if len(points) == 1:
            return 0.0
        if len(points) == 2:
            return abs(points[0] - points[1])

        # x軸方向に最も遠い点対
        si = points.index(min(points, key=lambda p: (p.x, p.y)))
        sj = points.index(max(points, key=lambda p: (p.x, p.y)))
        n = len(points)

        ret = 0.0
        # 半周回転
        i, j = si, sj
        while i != sj or j != si:
            ret = max(ret, abs(points[i] - points[j]))
            ni = (i + 1) % n
            nj = (j + 1) % n
            # 2つの辺が並行になる方向にずらす
            if (points[ni] - points[i]).det(points[nj] - points[j]) > 0:
                j = nj
            else:
                i = ni
        return ret

    def convex_cut_by_line(self, line_p1, line_p2):
        """
        凸多角形を直線 line_p1-line_p2 でカットする。
        凸じゃないといけません
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_4_C&lang=ja
        :param line_p1:
        :param line_p2:
        :return: (line_p1-line_p2 の左側の多角形, line_p1-line_p2 の右側の多角形)
        :rtype: (Polygon|None, Polygon|None)
        """
        n = len(self.points)
        line = Line.from_segment(line_p1, line_p2)
        # 直線と重なる点
        on_line_points = []
        for i, p in enumerate(self.points):
            if line.has_point(p):
                on_line_points.append(i)

        # 辺が直線上にある
        has_on_line_edge = False
        if len(on_line_points) >= 3:
            has_on_line_edge = True
        elif len(on_line_points) == 2:
            # 直線上にある点が隣り合ってる
            has_on_line_edge = abs(on_line_points[0] - on_line_points[1]) in [1, n - 1]
        # 辺が直線上にある場合、どっちか片方に全部ある
        if has_on_line_edge:
            for p in self.points:
                ccw = Point.ccw(line_p1, line_p2, p)
                if ccw == Point.CCW_COUNTER_CLOCKWISE:
                    return Polygon(self.points[:]), None
                if ccw == Point.CCW_CLOCKWISE:
                    return None, Polygon(self.points[:])

        ret_lefts = []
        ret_rights = []
        d = line_p2 - line_p1
        for p, q in self.iter2():
            det_p = d.det(p - line_p1)
            det_q = d.det(q - line_p1)
            if det_p > -EPS:
                ret_lefts.append(p)
            if det_p < EPS:
                ret_rights.append(p)
            # 外積の符号が違う == 直線の反対側にある場合は交点を追加
            if det_p * det_q < -EPS:
                intersection = line.intersection_point(Line.from_segment(p, q))
                ret_lefts.append(intersection)
                ret_rights.append(intersection)

        # 点のみの場合を除いて返す
        l = Polygon(ret_lefts) if len(ret_lefts) > 1 else None
        r = Polygon(ret_rights) if len(ret_rights) > 1 else None
        return l, r


def closest_pair(points):
    """
    最近点対 O(N log N)
    Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_5_A&lang=ja
    :param list of Point points:
    :rtype: (float, (Point, Point))
    :return: (距離, 点対)
    """
    assert len(points) >= 2

    def _rec(xsorted):
        """
        :param list of Point xsorted:
        :rtype: (float, (Point, Point))
        """
        n = len(xsorted)
        if n <= 2:
            return xsorted[0].dist(xsorted[1]), (xsorted[0], xsorted[1])
        if n <= 3:
            # 全探索
            d = INF
            pair = None
            for p, q in itertools.combinations(xsorted, r=2):
                if p.dist(q) < d:
                    d = p.dist(q)
                    pair = p, q
            return d, pair

        # 分割統治
        # 両側の最近点対
        ld, lp = _rec(xsorted[:n // 2])
        rd, rp = _rec(xsorted[n // 2:])
        if ld <= rd:
            d = ld
            ret_pair = lp
        else:
            d = rd
            ret_pair = rp

        mid_x = xsorted[n // 2].x
        # 中央から d 以内のやつを集める
        mid_points = []
        for p in xsorted:
            # if abs(p.x - mid_x) < d:
            if abs(p.x - mid_x) - d < -EPS:
                mid_points.append(p)

        # この中で距離が d 以内のペアがあれば更新
        mid_points.sort(key=lambda p: p.y)
        mid_n = len(mid_points)
        for i in range(mid_n - 1):
            j = i + 1
            p = mid_points[i]
            q = mid_points[j]
            # while q.y - p.y < d
            while (q.y - p.y) - d < -EPS:
                pq_d = p.dist(q)
                if pq_d < d:
                    d = pq_d
                    ret_pair = p, q
                j += 1
                if j >= mid_n:
                    break
                q = mid_points[j]
        return d, ret_pair

    return _rec(list(sorted(points, key=lambda p: p.x)))


def closest_pair_randomized(points):
    """
    最近点対 乱択版 O(N)
    http://ir5.hatenablog.com/entry/20131221/1387557630
    グリッドの管理が dict だから定数倍気になる
    Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_5_A&lang=ja
    :param list of Point points:
    :rtype: (float, (Point, Point))
    :return: (距離, 点対)
    """
    n = len(points)
    assert n >= 2
    if n == 2:
        return points[0].dist(points[1]), (points[0], points[1])

    # 逐次構成法
    points = points[:]
    random.shuffle(points)

    DELTA_XY = list(itertools.product([-1, 0, 1], repeat=2))
    grid = defaultdict(list)
    delta = INF
    dist = points[0].dist(points[1])
    ret_pair = points[0], points[1]
    for i in range(2, n):
        if delta < EPS:
            return 0.0, ret_pair
        # i 番目より前までを含む grid を構築
        # if dist < delta:
        if dist - delta < -EPS:
            delta = dist
            grid = defaultdict(list)
            for a in points[:i]:
                grid[a.x // delta, a.y // delta].append(a)
        else:
            p = points[i - 1]
            grid[p.x // delta, p.y // delta].append(p)

        p = points[i]
        dist = delta
        grid_x = p.x // delta
        grid_y = p.y // delta
        # 周り 9 箇所だけ調べれば OK
        for dx, dy in DELTA_XY:
            for q in grid[grid_x + dx, grid_y + dy]:
                d = p.dist(q)
                # if d < dist:
                if d - dist < -EPS:
                    dist = d
                    ret_pair = p, q
    return min(delta, dist), ret_pair


class Circle:
    def __init__(self, o, r):
        """
        :param Point o:
        :param float r:
        """
        self.o = o
        self.r = r

    def __eq__(self, other):
        return self.o == other.o and abs(self.r - other.r) < EPS

    def ctc(self, c):
        """
        共通接線 common tangent の数
        4: 離れてる
        3: 外接
        2: 交わってる
        1: 内接
        0: 内包
        inf: 同一
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_7_A&lang=ja
        :param Circle c:
        :rtype: int
        """
        if self.o == c.o:
            return INF if abs(self.r - c.r) < EPS else 0
        # 円同士の距離
        d = self.o.dist(c.o) - self.r - c.r
        if d > EPS:
            return 4
        elif d > -EPS:
            return 3
        # elif d > -min(self.r, c.r) * 2:
        elif d + min(self.r, c.r) * 2 > EPS:
            return 2
        elif d + min(self.r, c.r) * 2 > -EPS:
            return 1
        return 0

    def has_point_on_edge(self, p):
        """
        指定した点が円周上にあるか
        :param Point p:
        :rtype: bool
        """
        return abs(self.o.dist(p) - self.r) < EPS

    def contains(self, p, allow_on_edge=True):
        """
        指定した点を含むか
        :param Point p:
        :param bool allow_on_edge: 辺上の点を許容するか
        """
        if allow_on_edge:
            # return self.o.dist(p) <= self.r
            return self.o.dist(p) - self.r < EPS
        else:
            # return self.o.dist(p) < self.r
            return self.o.dist(p) - self.r < -EPS

    def area(self):
        """
        面積
        """
        return self.r ** 2 * PI

    def circular_segment_area(self, angle):
        """
        弓形⌓の面積
        :param float angle: 角度ラジアン
        """
        # 扇形の面積
        sector_area = self.area() * angle / TAU
        # 三角形部分を引く
        return sector_area - self.r ** 2 * math.sin(angle) / 2

    def intersection_points(self, other, allow_outer=False):
        """
        :param Segment|Circle other:
        :param bool allow_outer:
        """
        if isinstance(other, Segment):
            return self.intersection_points_with_segment(other, allow_outer=allow_outer)
        if isinstance(other, Circle):
            return self.intersection_points_with_circle(other)
        raise NotImplementedError()

    def intersection_points_with_segment(self, s, allow_outer=False):
        """
        線分と交差する点のリスト
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_7_D&lang=ja
        :param Segment s:
        :param bool allow_outer: 線分の間にない点を含む
        :rtype: list of Point
        """
        # 垂線の足
        projection_point = self.o.projection_point(s.p1, s.p2, allow_outer=True)
        # 線分との距離
        dist = self.o.dist(projection_point)
        # if dist > self.r:
        if dist - self.r > EPS:
            return []
        if dist - self.r > -EPS:
            if allow_outer or s.has_point(projection_point):
                return [projection_point]
            else:
                return []
        # 足から左右に diff だけ動かした座標が答え
        diff = Point.from_polar(math.sqrt(self.r ** 2 - dist ** 2), s.phase())
        ret1 = projection_point + diff
        ret2 = projection_point - diff
        ret = []
        if allow_outer or s.has_point(ret1):
            ret.append(ret1)
        if allow_outer or s.has_point(ret2):
            ret.append(ret2)
        return ret

    def intersection_points_with_circle(self, other):
        """
        円と交差する点のリスト
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_7_E&langja
        :param circle other:
        :rtype: list of Point
        """
        ctc = self.ctc(other)
        if not 1 <= ctc <= 3:
            return []
        if ctc == 3:
            # 外接
            return [Point.from_polar(self.r, (other.o - self.o).phase()) + self.o]
        if ctc == 1:
            # 内接
            if self.r > other.r:
                return [Point.from_polar(self.r, (other.o - self.o).phase()) + self.o]
            else:
                return [Point.from_polar(self.r, (self.o - other.o).phase()) + self.o]
        # 2つ交点がある
        assert ctc == 2

        a = other.r
        b = self.r
        c = self.o.dist(other.o)
        # 余弦定理で cos(a) を求めます
        cos_a = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        angle = math.acos(cos_a)
        phi = (other.o - self.o).phase()
        return [
            self.o + Point.from_polar(self.r, phi + angle),
            self.o + Point.from_polar(self.r, phi - angle),
        ]

    def tangent_points_with_point(self, p):
        """
        p を通る接線との接点
        :param Point p:
        :rtype: list of Point
        """
        dist = self.o.dist(p)
        # if dist < self.r:
        if dist - self.r < -EPS:
            # p が円の内部にある
            return []
        if dist - self.r < EPS:
            # p が円周上にある
            return [Point(p.x, p.y)]

        a = math.sqrt(dist ** 2 - self.r ** 2)
        b = self.r
        c = dist
        # 余弦定理で cos(a) を求めます
        cos_a = (b ** 2 + c ** 2 - a ** 2) / (2 * b * c)
        angle = math.acos(cos_a)
        phi = (p - self.o).phase()
        return [
            self.o + Point.from_polar(self.r, phi + angle),
            self.o + Point.from_polar(self.r, phi - angle),
        ]

    def tangent_points_with_circle(self, other):
        """
        other との共通接線との接点
        :param Circle other:
        :rtype: list of Point
        """
        ctc = self.ctc(other)
        if ctc > 4:
            raise ValueError('2つの円が同一です')
        if ctc == 0:
            return []
        if ctc == 1:
            return self.intersection_points_with_circle(other)

        assert ctc in (2, 3, 4)
        ret = []
        # 共通外接線を求める
        # if self.r == other.r:
        if abs(self.r - other.r) < EPS:
            # 半径が同じ == 2つの共通外接線が並行
            phi = (other.o - self.o).phase()
            ret.append(self.o + Point.from_polar(self.r, phi + PI / 2))
            ret.append(self.o + Point.from_polar(self.r, phi - PI / 2))
        else:
            # 2つの共通外接線の交点から接線を引く
            intersection = self.o + (other.o - self.o) / (self.r - other.r) * self.r
            ret += self.tangent_points_with_point(intersection)

        # 共通内接線を求める
        # 2つの共通内接線の交点から接線を引く
        intersection = self.o + (other.o - self.o) / (self.r + other.r) * self.r
        ret += self.tangent_points_with_point(intersection)
        return ret

    @staticmethod
    def circumscribed_of(p1, p2, p3):
        """
        p1・p2・p3 のなす三角形の外接円
        Verify:
        :param Point p1:
        :param Point p2:
        :param Point p3:
        """
        if p1.on_segment(p2, p3):
            return Circle((p2 + p3) / 2, p2.dist(p3) / 2)
        if p2.on_segment(p1, p3):
            return Circle((p1 + p3) / 2, p1.dist(p3) / 2)
        if p3.on_segment(p1, p2):
            return Circle((p1 + p2) / 2, p1.dist(p2) / 2)
        o = Point.circumstance_of(p1, p2, p3)
        return Circle(o, o.dist(p1))

    @staticmethod
    def min_enclosing(points):
        """
        points をすべて含む最小の円
        計算量の期待値は O(N)
        https://www.jaist.ac.jp/~uehara/course/2014/i481f/pdf/ppt-7.pdf
        Verify: https://www.spoj.com/problems/QCJ4/
        :param list of Point points:
        :rtype: Circle
        """
        points = points[:]
        random.shuffle(points)

        # 前から順番に決めて大きくしていく
        ret = Circle(points[0], 0)
        for i, p in enumerate(points):
            if ret.contains(p):
                continue
            ret = Circle(p, 0)
            for j, q in enumerate(points[:i]):
                if ret.contains(q):
                    continue
                # 2点を直径とする円
                ret = Circle((p + q) / 2, abs(p - q) / 2)
                for k, r in enumerate(points[:j]):
                    if ret.contains(r):
                        continue
                    # 3点に接する円
                    ret = Circle.circumscribed_of(p, q, r)
        return ret
