from collections import Counter, deque
from fractions import gcd
from functools import lru_cache
from functools import reduce
import functools
import heapq
import itertools
import math
import numpy as np
import sys

sys.setrecursionlimit(10000)
INF = float('inf')

I = lambda: int(input())
IF = lambda: float(input())
IS = lambda: input()
IL = lambda: list(map(int, input().split()))
ILF = lambda: list(map(float, input().split()))
ILS = lambda: input().split()
Yesif = lambda cond: print('Yes' if cond else 'No')
YESIF = lambda cond: print('YES' if cond else 'NO')
yesif = lambda cond: print('yes' if cond else 'no')
