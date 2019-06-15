import bisect
import os
from collections import Counter, deque
from fractions import gcd
from functools import lru_cache
from functools import reduce
import functools
import heapq
import itertools
import math
import numpy as np
import re
import string
import sys

if os.getenv("LOCAL"):
    sys.stdin = open("_in.txt", "r")

sys.setrecursionlimit(2147483647)
INF = float("inf")
