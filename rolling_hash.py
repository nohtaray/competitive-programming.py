class RollingHash:
    # Verify: http://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=ALDS1_14_B
    def __init__(self, seq, base=10 ** 9 + 7, mod=2 ** 89 - 1):
        """
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
