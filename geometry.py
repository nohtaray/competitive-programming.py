import cmath
import math

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

    def __init__(self, c: complex):
        self.c = c

    @property
    def x(self):
        return self.c.real

    @property
    def y(self):
        return self.c.imag

    @staticmethod
    def from_rect(x: float, y: float):
        return Point(complex(x, y))

    @staticmethod
    def from_polar(r: float, phi: float):
        return Point(cmath.rect(r, phi))

    def __add__(self, p):
        """
        :param Point p:
        """
        return Point(self.c + p.c)

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
        return Point(self.c - p.c)

    def __isub__(self, p):
        """
        :param Point p:
        """
        self.c -= p.c
        return self

    def __mul__(self, f: float):
        return Point(self.c * f)

    def __imul__(self, f: float):
        self.c *= f
        return self

    def __truediv__(self, f: float):
        return Point(self.c / f)

    def __itruediv__(self, f: float):
        self.c /= f
        return self

    def __repr__(self):
        return "({}, {})".format(round(self.x, 10), round(self.y, 10))

    def __neg__(self):
        return Point(-self.c)

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
        return abs(Point.from_rect(self.a, self.b).det(Point.from_rect(l.a, l.b))) < EPS

    def is_orthogonal_to(self, l):
        """
        直行しているかどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_A&lang=ja
        :param Line l:
        """
        # 法線ベクトル同士の内積がゼロ
        return abs(Point.from_rect(self.a, self.b).dot(Point.from_rect(l.a, l.b))) < EPS

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
        return Point.from_rect(x, y)

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
        return cmath.phase(self.p2 - self.p1)

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
            det_lower = EPS if allow_side else -EPS
            ok = True
            # self の両側に s.p1 と s.p2 があるか
            ok &= (self.p2 - self.p1).det(s.p1 - self.p1) * (self.p2 - self.p1).det(s.p2 - self.p1) < det_lower
            # s の両側に self.p1 と self.p2 があるか
            ok &= (s.p2 - s.p1).det(self.p1 - s.p1) * (s.p2 - s.p1).det(self.p2 - s.p1) < det_lower
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
        ret = [None] * (N * 2)
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
