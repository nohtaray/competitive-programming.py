import bisect
import heapq
import itertools
import math
import os
import re
import string
import sys
from collections import Counter, deque, defaultdict
from fractions import gcd
from functools import lru_cache, reduce

import numpy as np

if os.getenv("LOCAL"):
    sys.stdin = open("_in.txt", "r")

sys.setrecursionlimit(2147483647)
INF = float("inf")
