from scipy import signal
import numpy as np


# np.fft より速そう
# https://atcoder.jp/contests/abc291/submissions?f.Task=abc291_g&f.LanguageName=&f.Status=&f.User=nohtaray
def fft(A, B):
    return signal.fftconvolve(A, B)


def fft_int(A, B):
    return np.rint(fft(A, B)).astype(int)


def np_fft(A, B):
    N = max(len(A), len(B))
    fft_size = 1 << N.bit_length() + 1
    return np.fft.irfft(np.fft.rfft(A, fft_size) * np.fft.rfft(B, fft_size))


def np_fft_int(A, B):
    return np.array(np.rint(np_fft(A, B)), dtype=int)
