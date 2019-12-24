import functools
import os
import random

import matplotlib.patches as pat
import matplotlib.pyplot as plt
import networkx as nx

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
        elif type(f).__name__ == geo.Line.__name__:
            raise NotImplementedError()
        else:
            raise NotImplementedError()
    plt.axis('scaled')
    ax.set_aspect('equal')
    plt.show()


def generate_undirected_graph(V, E):
    """
    V 頂点 E 辺の単純連結無向グラフ
    :param int V:
    :param int E:
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
    return list(G.edges())


def generate_directed_graph(V, E):
    """
    V 頂点 E 辺の単純連結有向グラフ
    :param int V:
    :param int E:
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
    return list(G.edges())


def generate_oriented_graph(V, E):
    """
    両方向の辺がある頂点対を持たない有向グラフを生成
    https://en.wikipedia.org/wiki/Directed_graph#Types_of_directed_graphs
    :param int V:
    :param int E:
    :rtype: list of (int, int)
    """
    ret = []
    for v, u in generate_undirected_graph(V, E):
        if random.randint(0, 1):
            v, u = u, v
        ret.append((v, u))
    return ret


def plot_graph(edges, directed=False, weighted=False):
    """
    :param list of tuple edges:
    :param bool directed:
    :param bool weighted:
    """
    if weighted:
        raise NotImplementedError()
    cls = nx.DiGraph if directed else nx.Graph
    G = nx.from_edgelist(edges, cls)
    nx.draw(G)
    plt.show()
