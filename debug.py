import functools
import os

import matplotlib.patches as pat
import matplotlib.pyplot as plt

import libs.geometry as geo


def debug(fn):
    if not os.getenv("LOCAL"):
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        ret = fn(*args, **kwargs)
        print(
            "DEBUG: {}({}) -> ".format(
                fn.__name__,
                ", ".join(
                    list(map(str, args))
                    + ["{}={}".format(k, str(v)) for k, v in kwargs.items()]
                ),
            ),
            end="",
        )
        print(ret)
        return ret

    return wrapper


def plot_figure(*figures):
    alpha = 0.4
    ax = plt.axes()
    for f in figures:
        # isinstance だとコピペしたクラスが別のクラスとして扱われてしまうのでクラス名で文字列比較
        if type(f).__name__ == geo.Polygon.__name__:
            ax.add_patch(pat.Polygon([(p.x, p.y) for p in f.points], alpha=alpha))
        elif type(f).__name__ == geo.Circle.__name__:
            ax.add_patch(pat.Circle((f.o.x, f.o.y), f.r, alpha=alpha))
        elif type(f).__name__ == geo.Segment.__name__:
            ax.plot((f.p1.x, f.p2.x), (f.p1.y, f.p2.y))
        elif type(f).__name__ == geo.Point.__name__:
            ax.plot((f.x,), (f.y,), 'o')
        elif type(f).__name__ == geo.Line.__name__:
            raise NotImplementedError()
        else:
            raise NotImplementedError()
    plt.axis('scaled')
    ax.set_aspect('equal')
    plt.show()
