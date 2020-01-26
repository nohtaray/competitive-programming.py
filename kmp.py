class KMP:
    def __init__(self, needle):
        """
        https://ja.wikipedia.org/wiki/クヌース–モリス–プラット法
        :param typing.Sequence needle: 何を検索するか
        """
        self._needle = needle
        kmp = [0] * (len(needle) + 2)
        kmp[0] = -1
        kmp[1] = 0
        i = 2
        j = 0
        while i < len(needle):
            if needle[i - 1] == needle[j]:
                kmp[i] = j + 1
                i += 1
                j += 1
            elif j > 0:
                j = kmp[j]
            else:
                kmp[i] = 0
                i += 1
        self._kmp = kmp

    def index_of(self, haystack, m=0, i=0):
        """
        m + (haystack[m:] の何番目に needle があるか)
        見つからなければ -1
        needle[i:] のみ比較する
        :param typing.Sequence haystack: 何から検索するか
        :param int m: The position of the current character in haystack
        :param int i: The position of the current character in needle
        :rtype: int
        """
        while m + i < len(haystack):
            if self._needle[i] == haystack[m + i]:
                i += 1
                if i == len(self._needle):
                    return m
            else:
                m += i - self._kmp[i]
                if i > 0:
                    i = self._kmp[i]
        return -1

    def search(self, haystack):
        """
        ret[i]: haystack[i:i+len(needle)] == needle
        :param typing.Sequence haystack: 何から検索するか
        :rtype: list of bool
        """
        ret = [False] * len(haystack)
        m = 0
        i = 0
        while m + i < len(haystack):
            m = self.index_of(haystack, m=m, i=i)
            if m < 0:
                break
            ret[m] = True
            m += len(self._needle) - self._kmp[len(self._needle) - 1] - 1
            i = max(0, self._kmp[len(self._needle) - 1])
        return ret
