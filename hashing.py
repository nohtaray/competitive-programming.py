import random


class RollingHash:
    # Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_14_B
    def __init__(self, seq, base=37, mod=2 ** 61 - 1):
        """
        64bit を超えるとハッシュの構築だけで死ぬほど重くなるので避ける
        https://atcoder.jp/contests/abc284/submissions/41589904
        :param str|typing.Sequence[int] seq:
        :param int base:
        :param int mod:
        """
        if isinstance(seq, str):
            self._seq = seq = list(map(ord, seq))
        else:
            self._seq = seq
        self._base = base
        self._mod = mod

        hashes = [0] * (len(seq) + 1)
        power = [1] * (len(seq) + 1)
        for i, c in enumerate(seq):
            hashes[i + 1] = (hashes[i] * base + c) % mod
            power[i + 1] = power[i] * base % mod
        self._hashes = hashes
        self._power = power

    def get(self, L, r):
        """
        [L, r) のハッシュ値を取得します
        :param int L:
        :param int r:
        """
        if L >= r:
            return 0
        return (self._hashes[r] - self._hashes[L] * self._power[r - L]) % self._mod

    def lcp(self, p, q, allow_overlap=False):
        """
        seq[p:] と seq[q:] の Longest Common Prefix の長さ
        O(logN)
        :param int p:
        :param int q:
        :param bool allow_overlap:
        """
        lim = min(len(self._seq) - p, len(self._seq) - q)
        if not allow_overlap:
            lim = min(lim, abs(p - q))

        ok = 0
        ng = lim + 1
        while abs(ng - ok) > 1:
            sz = (ok + ng) // 2
            if self.get(p, p + sz) == self.get(q, q + sz):
                ok = sz
            else:
                ng = sz
        return ok

    def lcs(self, p, q, allow_overlap=False):
        """
        seq[:p] と seq[:q] の Longest Common Suffix の長さ
        O(logN)
        :param int p:
        :param int q:
        :param bool allow_overlap:
        """
        lim = min(p, q)
        if not allow_overlap:
            lim = min(lim, abs(p - q))

        ok = 0
        ng = lim + 1
        while abs(ng - ok) > 1:
            sz = (ok + ng) // 2
            if self.get(p - sz, p) == self.get(q - sz, q):
                ok = sz
            else:
                ng = sz
        return ok

    def concat(self, s1, s2, s2_len):
        """
        ハッシュ 2 つを結合する
        :param s1:
        :param s2:
        :param s2_len
        """
        return (s1 * self._power[s2_len] + s2) % self._mod


class ZobristHash:
    def __init__(self, items, mod=2 ** 61 - 1):
        """
        :param typing.Iterable[typing.Hashable] items:
        :param int mod:
        """
        # テーブル構築
        seen = set()
        table = {}
        for a in items:
            if a in table:
                continue
            h = random.randint(1, mod - 1)
            while h in seen:
                h = random.randint(1, mod - 1)
            seen.add(h)
            table[a] = h
        self._table = table
        self._mod = mod

    @property
    def table(self):
        """
        :rtype: dict[typing.Hashable, int]
        """
        return self._table

    def calc(self, items):
        """
        O(|items|)
        ハッシュ値を取得します
        items は同じ要素を含んではいけない
        別インスタンスから作ったハッシュは異なる値になる
        :param typing.Iterable[typing.Hashable] items:
        :rtype: int
        """
        ret = 0
        for a in items:
            ret ^= self._table[a]
        return ret

    def accumulate(self, items):
        """
        O(|items|)
        先頭から累積ハッシュ値を取得します
        items は同じ要素を含んではいけない
        別インスタンスから作ったハッシュは異なる値になる
        :param typing.Sequence[typing.Hashable] items:
        :rtype: typing.List[int]
        """
        ret = [0] * (len(items) + 1)
        hash = 0
        for i, a in enumerate(items, start=1):
            hash ^= self._table[a]
            ret[i] = hash
        return ret

    def concat(self, hash1, hash2):
        """
        ハッシュ 2 つを結合する
        :param int hash1:
        :param int hash2:
        :rtype: int
        """
        return hash1 ^ hash2

    def add(self, hash, item):
        """
        ハッシュに要素を追加する
        :param int hash:
        :param typing.Hashable item:
        :rtype: int
        """
        return hash ^ self._table[item]

    def remove(self, hash, item):
        """
        ハッシュから要素を削除する
        :param hash:
        :param item:
        :rtype: int
        """
        return hash ^ self._table[item]


class SequenceZobristHash:
    def __init__(self, seq, mod=2 ** 61 - 1):
        """
        連続する部分列を多重集合としてハッシュを取る
        https://atcoder.jp/contests/abc367/editorial/10692
        :param str|typing.Sequence[int] seq:
        :param int mod:
        """
        if isinstance(seq, str):
            self._seq = seq = list(map(ord, seq))
        else:
            self._seq = seq
        self._mod = mod

        # テーブル構築
        seen = set()
        a2h = {}
        for a in seq:
            if a in a2h:
                continue
            h = random.randint(1, mod - 1)
            while h in seen:
                h = random.randint(1, mod - 1)
            seen.add(h)
            a2h[a] = h

        # 累積和
        cum = [0] * (len(seq) + 1)
        s = 0
        for i, a in enumerate(seq):
            s += a2h[a]
            s %= mod
            cum[i + 1] = s
        self._cum = cum

    def get(self, l, r):
        """
        [l, r) のハッシュ値を取得します
        :param int l:
        :param int r:
        """
        if l >= r:
            return 0
        return (self._cum[r] - self._cum[l]) % self._mod

    def concat(self, s1, s2):
        """
        ハッシュ 2 つを結合する
        :param s1:
        :param s2:
        """
        return (s1 + s2) % self._mod
