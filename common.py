import bisect
import cmath
import heapq
import itertools
import math
import operator
import os
import random
import re
import string
import sys
from collections import Counter, defaultdict, deque
from copy import deepcopy
from decimal import Decimal
from fractions import Fraction
from functools import cache, reduce, cmp_to_key
from itertools import accumulate
from math import gcd
from operator import add, itemgetter, mul, xor
from typing import List, Tuple, Dict

import atcoder.convolution
import atcoder.dsu
import atcoder.fenwicktree
import atcoder.lazysegtree
import atcoder.math
import atcoder.maxflow
import atcoder.mincostflow
import atcoder.modint
import atcoder.scc
import atcoder.segtree
import atcoder.string
import atcoder.twosat
import numpy as np

if os.getenv("LOCAL"):
    sys.stdin = open("_in.txt", "r")

sys.set_int_max_str_digits(0)
sys.setrecursionlimit(10**9)
INF = float("inf")
IINF = 10**18
# MOD = 10**9 + 7
MOD = 998244353
