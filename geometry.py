import cmath

INF = float("inf")
PI = cmath.pi
TAU = cmath.pi * 2
EPS = 1e-8


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
        p に向かってる状態から q まで反時計回りに回転するときの角度
        :param Point p:
        :param Point q:
        :rtype: float
        """
        return (cmath.phase(q.c - self.c) - cmath.phase(p.c - self.c)) % TAU

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
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_B&lang=ja
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_C&lang=ja
        FIXME: 誤差が気になる。EPS <= 1e-9 だと CGL_2_B ダメだった。
        :param l:
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

    def intersects_with(self, s, allow_side=True):
        """
        交差するかどうか
        Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=CGL_2_B&lang=ja
        :param Segment s:
        :param allow_side: 端っこでギリギリ触れているのを許容するか
        """
        l1 = Line.from_segment(self.p1, self.p2)
        l2 = Line.from_segment(s.p1, s.p2)
        if l1.is_parallel_to(l2):
            # 並行なら線分の端点がもう片方の線分の上にあるかどうか
            return (s.p1.on_segment(self.p1, self.p2, allow_side) or
                    s.p2.on_segment(self.p1, self.p2, allow_side) or
                    self.p1.on_segment(s.p1, s.p2, allow_side) or
                    self.p2.on_segment(s.p1, s.p2, allow_side))
        else:
            # 直線同士の交点が線分の上にあるかどうか
            p = l1.intersection_point(l2)
            return p.on_segment(self.p1, self.p2, allow_side) and p.on_segment(s.p1, s.p2, allow_side)

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
