def make_trie(str_set):
    """
    トライ木
    もうちょいいい感じにしたい
    https://atcoder.jp/contests/arc087/submissions/5329903

    :param collections.Iterable[str] str_set:
    :rtype: dict of dict
    """
    trie = {}
    for s in str_set:
        node = trie
        for c in s:
            if c not in node:
                node[c] = {}
            node = node[c]
    return trie
