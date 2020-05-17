from libs.sparse_table import SparseTable


class LineTree:
    def __init__(self, tree, fn=min):
        """
        木上のパスの辺に fn を適用する
        構築 O(N log N)、クエリ O(1)
        https://codeforces.com/blog/entry/71568?#comment-559304
        HL 分解で代用できそう
        Verify: https://atcoder.jp/contests/past202004-open/submissions/13279427
        :param list of (list of (int, int)) tree: (to, weight) の隣接リスト
        :param callable fn:
        """
        if not (fn is min or fn is max):
            raise NotImplementedError()
        self._tree = tree
        self._size = len(tree)
        self._fn = fn

        self._build()

    def _build(self):
        edges = []
        for v in range(len(self._tree)):
            for u, w in self._tree[v]:
                edges.append((w, v, u))
        if self._fn is max:
            edges.sort()
        elif self._fn is min:
            edges.sort(reverse=True)
        else:
            assert False

        list_ptr = [[] for _ in range(len(self._tree))]
        vertices = {}
        for v, li in enumerate(list_ptr):
            vertices[id(li)] = [v]

        for w, v, u in edges:
            vli = list_ptr[v]
            uli = list_ptr[u]
            if vli is uli:
                continue

            # マージテクで併合
            if len(vli) < len(uli):
                vli, uli = uli, vli
            vli.append(w)
            vli += uli
            for u in vertices[id(uli)]:
                vertices[id(vli)].append(u)
                list_ptr[u] = vli

        idx = [-1] * len(self._tree)
        for i, v in enumerate(vertices[id(list_ptr[0])]):
            idx[v] = i

        self._idx = idx
        self._st = SparseTable(values=list_ptr[0], fn=self._fn)

    def query(self, v, u):
        """
        v と u を結ぶパス上の辺に fn を適用した結果
        :param int v:
        :param int u:
        """
        vi = self._idx[v]
        ui = self._idx[u]
        if vi > ui:
            vi, ui = ui, vi
        return self._st.get(vi, ui)
