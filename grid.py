import numpy as np


class Grid:
    def __init__(self, size):
        self._size = size
        self.grid = np.zeros((size, size))

    def draw(self, sx, sy, ex, ey):
        """
        grid の累積和をとったときの [(sx%size, sy%size), (ex%size, ey%size)) の範囲に 1 を加算する
        なんかに使えるかなあ
        https://atcoder.jp/contests/abc086/submissions/5395679
        :param int sx:
        :param int sy:
        :param int ex:
        :param int ey:
        :return:
        """
        sx %= self._size
        sy %= self._size
        ex = (ex - 1) % self._size + 1
        ey = (ey - 1) % self._size + 1

        if sx < ex and sy < ey:
            self.grid[sx, sy] += 1
            if ex < self._size:
                self.grid[ex, sy] -= 1
            if ey < self._size:
                self.grid[sx, ey] -= 1
            if ex < self._size and ey < self._size:
                self.grid[ex, ey] += 1

        elif ex <= sx:
            if ey <= sy:
                self.draw(0, 0, ex, ey)
                self.draw(0, sy, ex, self._size)
                self.draw(sx, 0, self._size, ey)
                self.draw(sx, sy, self._size, self._size)
            else:
                self.draw(0, sy, ex, ey)
                self.draw(sx, sy, self._size, ey)
        else:
            self.draw(sx, 0, ex, ey)
            self.draw(sx, sy, ex, self._size)
