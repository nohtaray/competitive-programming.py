from typing import Iterable, Iterator, List, Any


class RandomAccessDeque:
    """deque 互換の O(1) random-access リングバッファ"""

    __slots__ = ("_data", "_head", "_tail", "_size")

    # ---------- 基本 ----------
    def __init__(self, iterable: Iterable[Any] = (), init_capacity: int = 8):
        cap = 1
        while cap < init_capacity:  # 2 の冪に丸める（ビット演算高速化）
            cap <<= 1
        self._data: List[Any] = [None] * cap
        self._head = 0  # 先頭要素の物理インデックス
        self._tail = 0  # 末尾「次」位置
        self._size = 0
        for x in iterable:
            self.append(x)

    def __len__(self) -> int:
        return self._size

    def _capacity(self) -> int:
        return len(self._data)

    # ---------- 伸縮 ----------
    def _grow(self) -> None:  # 要素数==容量 で 2 倍化
        old_cap = self._capacity()
        new_cap = old_cap << 1
        new_data = [None] * new_cap
        mask = old_cap - 1
        for i in range(self._size):
            new_data[i] = self._data[(self._head + i) & mask]
        self._data = new_data
        self._head = 0
        self._tail = self._size

    # ---------- 追加 ----------
    def append(self, value: Any) -> None:  # 末尾
        if self._size == self._capacity():
            self._grow()
        self._data[self._tail] = value
        self._tail = (self._tail + 1) & (self._capacity() - 1)
        self._size += 1

    def appendleft(self, value: Any) -> None:  # 先頭
        if self._size == self._capacity():
            self._grow()
        self._head = (self._head - 1) & (self._capacity() - 1)
        self._data[self._head] = value
        self._size += 1

    # ---------- 削除 ----------
    def pop(self) -> Any:  # 末尾
        if not self._size:
            raise IndexError("pop from empty deque")
        self._tail = (self._tail - 1) & (self._capacity() - 1)
        val = self._data[self._tail]
        self._data[self._tail] = None
        self._size -= 1
        return val

    def popleft(self) -> Any:  # 先頭
        if not self._size:
            raise IndexError("pop from empty deque")
        val = self._data[self._head]
        self._data[self._head] = None
        self._head = (self._head + 1) & (self._capacity() - 1)
        self._size -= 1
        return val

    # ---------- ランダムアクセス ----------
    def __getitem__(self, idx):
        if isinstance(idx, slice):
            start, stop, step = idx.indices(self._size)
            return [self[i] for i in range(start, stop, step)]
        if idx < 0:
            idx += self._size
        if idx < 0 or idx >= self._size:
            raise IndexError("deque index out of range")
        mask = self._capacity() - 1
        return self._data[(self._head + idx) & mask]

    def __setitem__(self, idx, value):
        if idx < 0:
            idx += self._size
        if idx < 0 or idx >= self._size:
            raise IndexError("deque assignment index out of range")
        mask = self._capacity() - 1
        self._data[(self._head + idx) & mask] = value

    # ---------- 補助 ----------
    def __iter__(self) -> Iterator[Any]:
        for i in range(self._size):
            yield self[i]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({list(self)})"
