import atcoder.convolution
import numpy as np
from scipy import signal


# PyPy のときはこれを使う
# https://github.com/shakayami/ACL-for-python/blob/master/convolution.py
# https://atcoder.jp/contests/practice2/submissions/61290539


def fft(A, B):
    return signal.fftconvolve(A, B)


def fft_int(A, B):
    return np.rint(fft(A, B)).astype(np.int64)


def fft_mod(f, g, mod):
    """
    畳み込み
    係数および法は 2^30-2 程度まで
    NTT 素数でなくてもいい
    """
    f = np.asarray(f, dtype=np.int64)
    g = np.asarray(g, dtype=np.int64)
    N = len(f) + len(g) - 1

    MASK = (1 << 10) - 1
    # 10 bit ごとに切り出し
    f0, f1, f2 = f & MASK, (f >> 10) & MASK, f >> 20
    g0, g1, g2 = g & MASK, (g >> 10) & MASK, g >> 20

    # -------- FFT 畳み込み (6 回) --------
    fft = lambda a, b: np.rint(signal.fftconvolve(a, b)[:N]).astype(np.int64)
    p00 = fft(f0, g0) % mod  # f0 g0
    p11 = fft(f1, g1) % mod  # f1 g1
    p22 = fft(f2, g2) % mod  # f2 g2
    p01 = fft(f0 + f1, g0 + g1) % mod
    p02 = fft(f0 + f2, g0 + g2) % mod
    p12 = fft(f1 + f2, g1 + g2) % mod

    # -------- 合成 (c0 ... c4) --------
    c0 = p00
    c1 = (p01 - p00 - p11) % mod  # f0*g1 + f1*g0
    c2 = (p02 - p00 - p22 + p11) % mod  # f0*g2 + f1*g1 + f2*g0
    c3 = (p12 - p11 - p22) % mod  # f1*g2 + f2*g1
    c4 = p22  # f2*g2

    # -------- 桁上げ (基数 2^10) --------
    B1 = (1 << 10) % mod
    B2 = (1 << 20) % mod
    B3 = (1 << 30) % mod
    B4 = (1 << 40) % mod
    res = (c0 + c1 * B1 + c2 * B2 + c3 * B3 + c4 * B4) % mod
    return res.astype(np.int64)


# C++ 板
# https://atcoder.jp/contests/typical90/submissions/66803088
"""
ll inv_mod(ll a, ll mod) {
  ll res = 1, e = mod - 2;
  while (e > 0) {
    if (e & 1) res = res * a % mod;
    a = a * a % mod;
    e >>= 1;
  }
  return res;
}

vector<vector<ll>> matrix_mul_mod(const vector<vector<ll>> &m1, const vector<vector<ll>> &m2, ll mod) {
  int n = m1.size(), m = m2[0].size(), p = m2.size();
  vector<vector<ll>> res(n, vector<ll>(m));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
      for (int k = 0; k < p; k++)
        res[i][j] = (res[i][j] + m1[i][k] * m2[k][j]) % mod;
  return res;
}

vector<vector<ll>> matrix_power_mod(vector<vector<ll>> matrix, ll n, ll mod) {
  int sz = matrix.size();
  vector<vector<ll>> res(sz, vector<ll>(sz));
  for (int i = 0; i < sz; i++) res[i][i] = 1;
  while (n > 0) {
    if (n & 1) res = matrix_mul_mod(res, matrix, mod);
    matrix = matrix_mul_mod(matrix, matrix, mod);
    n >>= 1;
  }
  return res;
}

vector<ll> poly_mul(const vector<ll> &a1, const vector<ll> &a2, ll mod, ll max_deg = -1) {
  auto ret = convolution<MOD>(a1, a2);
  if (max_deg != -1 && (int) ret.size() > max_deg + 1) ret.resize(max_deg + 1);
  return ret;
}

vector<ll> poly_inv(const vector<ll> &f, int n, ll mod = MOD) {
  if (f[0] % mod == 0) throw invalid_argument("f[0] must be invertible");
  ll f0_inv = inv_mod(f[0], mod);
  vector<ll> g = {f0_inv};
  int k = 1;
  while (k < n) {
    int next_k = min(2 * k, n);
    auto g_squared = poly_mul(g, g, mod, next_k);
    vector<ll> f_part(f.begin(), f.begin() + min((int) f.size(), next_k));
    auto fg_squared = poly_mul(f_part, g_squared, mod, next_k);
    vector<ll> new_g(next_k);
    for (int i = 0; i < (int) g.size() && i < next_k; i++)
      new_g[i] = 2 * g[i] % mod;
    for (int i = 0; i < (int) fg_squared.size() && i < next_k; i++)
      new_g[i] = (new_g[i] - fg_squared[i] + mod) % mod;
    g = new_g;
    k = next_k;
  }
  g.resize(n);
  return g;
}

vector<ll> poly_add(const vector<ll> &a1, const vector<ll> &a2, ll mod) {
  vector<ll> ret(max(a1.size(), a2.size()));
  for (int i = 0; i < (int) a1.size(); i++) ret[i] = a1[i];
  for (int i = 0; i < (int) a2.size(); i++) {
    ret[i] += a2[i];
    if (ret[i] >= mod) ret[i] -= mod;
  }
  return ret;
}

pair<vector<ll>, vector<ll>> poly_div(const vector<ll> &f, const vector<ll> &g, ll mod = MOD) {
  int deg_f = f.size() - 1;
  while (deg_f >= 0 && f[deg_f] == 0) deg_f--;
  int deg_g = g.size() - 1;
  while (deg_g >= 0 && g[deg_g] == 0) deg_g--;
  if (deg_g == -1) throw invalid_argument("Division by zero polynomial");
  if (deg_f < deg_g) return {{}, f};
  int n = deg_f - deg_g + 1, m = deg_g + 1;
  vector<ll> rev_f(n), rev_g(m);
  for (int i = 0; i <= deg_f; i++) if (deg_f - i < n) rev_f[deg_f - i] = f[i];
  for (int i = 0; i <= deg_g; i++) rev_g[deg_g - i] = g[i];
  auto rev_g_inv = poly_inv(rev_g, n, mod);
  auto rev_q = poly_mul(rev_f, rev_g_inv, mod, n);
  vector<ll> q(n);
  for (int i = 0; i < n; i++) q[n - 1 - i] = rev_q[i];
  while (!q.empty() && q.back() == 0) q.pop_back();
  auto gq = poly_mul(g, q, mod);
  vector<ll> r = f;
  for (int i = 0; i < (int) gq.size() && i < (int) r.size(); i++)
    r[i] = (r[i] - gq[i] + mod) % mod;
  while (!r.empty() && r.back() == 0) r.pop_back();
  return {q, r};
}
"""


def poly_mul(a1, a2, mod, max_deg=None):
    """
    多項式の積
    C++ に変換推奨
    :param list of int a1:
    :param list of int a2:
    :param int mod:
    :param int|None max_deg: 最大次数
    :rtype: list of int
    """
    # ret = atcoder.convolution.convolution(mod, a1, a2)
    ret = fft_mod(a1, a2, mod)
    if max_deg is not None:
        return ret[: max_deg + 1]
    return ret


def poly_add(a1, a2, mod):
    """
    多項式の加算
    :param list of int a1:
    :param list of int a2:
    :param int mod:
    :rtype: list of int
    """
    ret = [0] * max(len(a1), len(a2))
    for i in range(len(a1)):
        ret[i] += a1[i]
    for i in range(len(a2)):
        ret[i] += a2[i]
        ret[i] %= mod
    return ret


def poly_inv(f, n, mod=998244353):
    """
    多項式 f の逆元を mod x^n で計算する
    :param list of int f: 多項式の係数リスト
    :param int n: 求める逆元の次数
    :param int mod: 係数の法
    :returns: f * g ≡ 1 (mod x^n) となる多項式gの係数リスト
    :rtype: list of int
    """
    # f[0]が0の場合は逆元が存在しない
    if f[0] % mod == 0:
        raise ValueError("f[0] must be invertible modulo p")

    # 定数項の逆元を計算（フェルマーの小定理）
    f0_inv = pow(f[0], mod - 2, mod)

    # 初期値: g ≡ f[0]^(-1) (mod x)
    g = [f0_inv]

    # kを2倍にしながら精度を上げていく
    k = 1
    while k < n:
        # 次のステップでの精度
        next_k = min(2 * k, n)

        # g_hat^2 を計算
        g_squared = poly_mul(g, g, mod, next_k)

        # f * g_hat^2 を計算
        fg_squared = poly_mul(f[:next_k], g_squared, mod, next_k)

        # g = 2*g_hat - f*g_hat^2 (mod x^{2k})
        new_g = [0] * next_k
        for i in range(min(len(g), next_k)):
            new_g[i] = (2 * g[i]) % mod
        for i in range(min(len(fg_squared), next_k)):
            new_g[i] = (new_g[i] - fg_squared[i]) % mod

        g = new_g
        k = next_k

    return g[:n]


def poly_div(f, g, mod=998244353):
    """
    多項式の除算 f(x) = g(x)q(x) + r(x) を計算
    :param list of int f: 被除数の多項式の係数リスト
    :param list of int g: 除数の多項式の係数リスト
    :param int mod: 係数の法（デフォルトはNTT素数998244353）
    :returns: (q, r) 商qと剰余rのタプル; deg(r) < deg(g) を満たす
    :rtype: tuple of (list of int, list of int)
    """

    # 次数を取得（最高次の非ゼロ係数を探す）
    def get_degree(poly):
        for i in range(len(poly) - 1, -1, -1):
            if poly[i] % mod != 0:
                return i
        return -1  # ゼロ多項式

    deg_f = get_degree(f)
    deg_g = get_degree(g)

    # gがゼロ多項式の場合
    if deg_g == -1:
        raise ValueError("Division by zero polynomial")

    # fの次数がgより小さい場合
    if deg_f < deg_g:
        return [], f[:]

    n = deg_f - deg_g + 1  # 商の次数+1
    m = deg_g + 1  # gの次数+1

    # rev(f) = f(x^-1) * x^(deg(f)) を計算
    # rev_f の最初のn項のみが必要
    rev_f = [0] * n
    for i in range(deg_f + 1):
        if i < len(f) and f[i] % mod != 0:
            idx = deg_f - i
            if idx < n:  # n項までしか必要ない
                rev_f[idx] = f[i]

    # rev(g) = g(x^-1) * x^(deg(g)) を計算
    rev_g = [0] * m
    for i in range(deg_g + 1):
        if i < len(g) and g[i] % mod != 0:
            rev_g[deg_g - i] = g[i]

    # rev(g)の逆元を mod x^n で計算
    rev_g_inv = poly_inv(rev_g, n, mod)

    # rev(q) = rev(f) / rev(g) mod x^n を計算
    rev_q = poly_mul(rev_f[:n], rev_g_inv, mod, n)

    # qを復元（rev(rev(q))）
    q = [0] * n
    for i in range(n):
        if i < len(rev_q) and rev_q[i] % mod != 0:
            q[n - 1 - i] = rev_q[i]

    # 商の次数を調整（leading zerosを除去）
    while len(q) > 1 and q[-1] % mod == 0:
        q.pop()

    # r = f - g*q を計算
    gq = poly_mul(g, q, mod)
    r = f[:]
    for i in range(min(len(gq), len(r))):
        r[i] = (r[i] - gq[i]) % mod

    # 剰余の次数を調整
    while len(r) > 0 and r[-1] % mod == 0:
        r.pop()

    return q, r


def poly_matrix_mul(m1, m2, mod, max_deg=None):
    """
    要素が多項式である行列の積
    C++ に変換推奨
    https://atcoder.jp/contests/abc409/submissions/66599005
    :param list of (list of (list of int)) m1:
    :param list of (list of (list of int)) m2:
    :param int mod:
    :param int|None max_deg: 最大次数
    :rtype: list of (list of (list of int))
    """
    rows = []
    for r1 in range(len(m1)):
        row = []
        for c2 in range(len(m2[0])):
            s = []
            for r2 in range(len(m2)):
                a = poly_mul(m1[r1][r2], m2[r2][c2], mod, max_deg)
                s = poly_add(s, a, mod)
            row.append(s)
        rows.append(row)
    return rows
