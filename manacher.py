def manacher(S):
    """
    S の各文字について、その文字を中心とする最長の回文の半径を返す
    :param str S:
    :returns list of int
    """
    i = 0
    j = 0
    R = [0] * len(S)
    while i < len(S):
        while i - j >= 0 and i + j < len(S) and S[i - j] == S[i + j]:
            j += 1
        R[i] = j
        k = 1
        while i - k >= 0 and k + R[i - k] < j:
            R[i + k] = R[i - k]
            k += 1
        i += k
        j -= k
    return R


def longest_palindrome(S):
    """
    S の部分文字列のうち最長の回文を返す
    :param str S:
    :return:
    """
    S = "$".join(S)
    R = manacher(S)
    max_len = 0
    max_pos = 0
    for i in range(len(S)):
        if R[i] > max_len:
            max_len = R[i]
            max_pos = i
    return S[max_pos - max_len + 1 : max_pos + max_len].replace("$", "")
