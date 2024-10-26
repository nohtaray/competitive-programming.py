import functools
import os
import random
from copy import deepcopy

import sys
import time
import matplotlib.patches as pat
import matplotlib.pyplot as plt
import networkx as nx
from decorator import contextmanager

import libs.geometry as geo


def debug(fn):
    if not os.getenv("LOCAL"):
        return fn

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        kwargs_cp = deepcopy(kwargs)
        ret = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        print("DEBUG [{:4d} ms]: {}({}) -> {}".format(
            int(elapsed_ms),
            fn.__name__,
            ", ".join(
                list(map(str, args))
                + ["{}={}".format(k, str(v)) for k, v in kwargs_cp.items()]
            ),
            ret
        ))
        return ret

    return wrapper


@contextmanager
def timer(name):
    st = time.perf_counter()
    yield
    t = int((time.perf_counter() - st) * 1000)
    print(f'[{name}] {t:4d} ms', file=sys.stderr)


def plot_figure(*figures):
    """
    geometry.py のクラスを matplotlib で描画
    :param figures:
    """
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
        elif isinstance(f, complex):
            ax.plot((f.real,), (f.imag,), 'o')
        elif type(f).__name__ == geo.Line.__name__:
            raise NotImplementedError()
        else:
            raise NotImplementedError()
    plt.axis('scaled')
    ax.set_aspect('equal')
    plt.show()


def generate_undirected_graph(V, E, origin=1):
    """
    V 頂点 E 辺の単純連結無向グラフ
    :param int V:
    :param int E:
    :param int origin:
    :rtype: list of (int, int)
    """
    if E < V - 1:
        raise ValueError('辺が少なすぎます')
    if E > V * (V - 1) // 2:
        raise ValueError('辺が多すぎます')

    #: :type: nx.Graph
    G = nx.random_tree(V)
    if V * (V - 1) // 2 <= 1e6:
        # 存在しない辺を全部とってきてその中から選ぶ
        edges = list(nx.non_edges(G))
        random.shuffle(edges)
        G.add_edges_from(edges[:E - V + 1])
    else:
        # 辺を適当に生成して存在しなければ追加
        cnt = V - 1
        while cnt < E:
            v = random.randint(0, V - 1)
            u = random.randint(0, V - 1)
            if v == u or G.has_edge(v, u):
                continue
            G.add_edge(v, u)
            cnt += 1
    ret = []
    for v, u in G.edges():
        ret.append((v + origin, u + origin))
    return ret


def generate_undirected_weighted_graph(V, E, max_weight, origin=1):
    """
    V 頂点 E 辺の重み付き単純連結無向グラフ
    :param int V:
    :param int E:
    :param int max_weight:
    :param int origin:
    :rtype: list of (int, int, int)
    """
    ret = []
    for a, b in generate_undirected_graph(V, E, origin=origin):
        ret.append((a, b, random.randint(1, max_weight)))
    return ret


def generate_directed_graph(V, E, origin=1):
    """
    V 頂点 E 辺の単純連結有向グラフ
    :param int V:
    :param int E:
    :param int origin:
    :rtype: list of (int, int)
    """
    if E < V - 1:
        raise ValueError('辺が少なすぎます')
    if E > V * (V - 1):
        raise ValueError('辺が多すぎます')

    tree = []
    for v, u in nx.random_tree(V).edges():
        if random.randint(0, 1):
            v, u = u, v
        tree.append((v, u))
    #: :type: nx.DiGraph
    G = nx.from_edgelist(tree, create_using=nx.DiGraph)
    if V * (V - 1) <= 1e6:
        # 存在しない辺を全部とってきてその中から選ぶ
        edges = list(nx.non_edges(G))
        random.shuffle(edges)
        G.add_edges_from(edges[:E - V + 1])
    else:
        # 辺を適当に生成して存在しなければ追加
        cnt = V - 1
        while cnt < E:
            v = random.randint(0, V - 1)
            u = random.randint(0, V - 1)
            if v == u or G.has_edge(v, u):
                continue
            G.add_edge(v, u)
            cnt += 1
    ret = []
    for v, u in G.edges():
        ret.append((v + origin, u + origin))
    return ret


def generate_oriented_graph(V, E, origin=1):
    """
    両方向の辺がある頂点対を持たない有向グラフを生成
    https://en.wikipedia.org/wiki/Directed_graph#Types_of_directed_graphs
    :param int V:
    :param int E:
    :param int origin:
    :rtype: list of (int, int)
    """
    ret = []
    for v, u in generate_undirected_graph(V, E, origin=origin):
        if random.randint(0, 1):
            v, u = u, v
        ret.append((v, u))
    return ret


def generate_tree(V, directed=False, origin=1):
    """
    V 頂点の木を生成する
    :param int V:
    :param bool directed:
    :param int origin:
    """
    if directed:
        return generate_directed_graph(V=V, E=V - 1, origin=origin)
    else:
        return generate_undirected_graph(V=V, E=V - 1, origin=origin)


def plot_graph(edges, directed=False):
    """
    :param typing.List[typing.Tuple[int]] edges: (from, to, [weight])
    :param bool directed:
    """
    if not edges:
        return
    weighted = len(edges[0]) == 3

    cls = nx.DiGraph if directed else nx.Graph
    G = cls()
    if weighted:
        G.add_weighted_edges_from(edges)
        pos = nx.spring_layout(G)
        labels = nx.draw_networkx_edge_labels(
            G, pos, edge_labels={(v, u): w for v, u, w in edges})
        for label in labels.values():
            # ラベルの傾きを修正
            label.set_rotation('horizontal')
        nx.draw_networkx(G, pos, with_labels=True, alpha=0.5)
    else:
        G.add_edges_from(edges)
        nx.draw_networkx(G, alpha=0.5)
    plt.axis("off")
    plt.show()
