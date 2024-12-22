import _bisect as bisect
import itertools


class LongestCommonSubsequence:
    # https://ja.wikipedia.org/wiki/最長共通部分列問題
    # Verify: https://atcoder.jp/contests/code-festival-2015-morning-middle/submissions/10986270
    def __init__(self, s, t):
        # s と t の LCS を求める
        self._s = s
        self._t = t

    def get(self):
        """
        O(|s||t||result|)
        :rtype: str
        """
        # dp[i + 1][j + 1]: s[:i] と t[:i] の最長共通部分列
        dp = [[''] * (len(self._t) + 1) for _ in range(len(self._s) + 1)]
        for i, j in itertools.product(range(len(self._s)), range(len(self._t))):
            if self._s[i] == self._t[j]:
                dp[i + 1][j + 1] = dp[i][j] + self._s[i]
            else:
                s = dp[i][j + 1]
                t = dp[i + 1][j]
                dp[i + 1][j + 1] = s if len(s) > len(t) else t
        return dp[len(self._s)][len(self._t)]

    def get_count(self):
        """
        O(|s||t|)
        :rtype: int
        """
        # dp[i + 1][j + 1]: s[:i] と t[:i] の最長共通部分列の長さ
        dp = [[0] * (len(self._t) + 1) for _ in range(len(self._s) + 1)]
        for i, j in itertools.product(range(len(self._s)), range(len(self._t))):
            if self._s[i] == self._t[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
        return dp[len(self._s)][len(self._t)]

    def get_count_of_permutation(self):
        """
        t に重複がないとき専用
        O(|s|log|t|)
        Verify: https://atcoder.jp/contests/arc189/submissions/61026429
        :rtype: int
        """
        inf = len(self._t)
        # s を t 上の位置に変換すると LIS になる
        pos = {c: i for i, c in enumerate(self._t)}
        sp = [pos[c] if c in pos else inf for c in self._s]
        dp = [inf] * (len(sp) + 1)
        for c in sp:
            dp[bisect.bisect_left(dp, c)] = c
        return bisect.bisect_left(dp, inf)
