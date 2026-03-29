# Copyright 2026 Ommkar Ankit Rout
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Persistent min-heap (priority queue) implementation with structural sharing.

A heap is a complete binary tree where every parent is less than or equal to its children.
This implementation keeps the underlying array immutable by storing it as a tuple and
creating a new tuple for every operation.
"""

from typing import Any, Iterable


class PersistentHeap:
    """
    Immutable persistent min-heap.

    Architecture:
        - Backed by a tuple representing the heap array (0-based indexing)
        - Structural sharing: original heaps remain untouched; new heaps reuse unchanged
          array segments where possible
        - Operations return new `PersistentHeap` instances

    Operations:
        - push: O(log n) insert
        - pop: O(log n) remove-min
        - peek: O(1) view-min
        - is_empty / len: O(1)

    Example:
        h0 = PersistentHeap()
        h1 = h0.push(5)
        h2 = h1.push(3)
        h3 = h2.push(10)

        top, h4 = h3.pop()   # top = 3, h4 still a valid heap
        assert h2.peek() == 3
    """

    __slots__ = ("_data",)

    def __init__(self, data: tuple[Any, ...] | None = None) -> None:
        self._data = data if data is not None else ()

    @classmethod
    def from_iterable(cls, values: Iterable[Any]) -> "PersistentHeap":
        """
        Build a heap from an iterable of values.

        Args:
            values: Elements to insert

        Returns:
            A new PersistentHeap containing all elements
        """
        heap: PersistentHeap = cls()
        for value in values:
            heap = heap.push(value)
        return heap

    # -------------------
    # Core Operations

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return len(self._data) == 0

    def __len__(self) -> int:  # pragma: no cover - trivial
        """Return the number of elements in the heap."""
        return len(self._data)

    def peek(self) -> Any:
        """
        View the smallest element without removing it.

        Raises:
            IndexError: If the heap is empty
        """
        if not self._data:
            raise IndexError("peek from empty heap")
        return self._data[0]

    def push(self, value: Any) -> "PersistentHeap":
        """
        Insert a value into the heap.

        Args:
            value: The value to insert

        Returns:
            A new PersistentHeap with the value inserted
        """
        data = list(self._data)
        data.append(value)
        self._sift_up(data, len(data) - 1)
        return PersistentHeap(tuple(data))

    def pop(self) -> tuple[Any, "PersistentHeap"]:
        """
        Remove and return the smallest value from the heap.

        Returns:
            Tuple of (min_value, new_heap)

        Raises:
            IndexError: If the heap is empty
        """
        if not self._data:
            raise IndexError("pop from empty heap")

        data = list(self._data)
        min_value = data[0]

        last = data.pop()  # Remove last element
        if not data:
            return min_value, PersistentHeap()

        data[0] = last
        self._sift_down(data, 0)
        return min_value, PersistentHeap(tuple(data))

    # -------------------
    # Utilities

    def to_list(self) -> list[Any]:
        """Return the internal heap array as a list (heap order)."""
        return list(self._data)

    def __repr__(self) -> str:  # pragma: no cover - representational
        return f"PersistentHeap({self.to_list()!r})"

    def __eq__(self, other: Any) -> bool:  # pragma: no cover - simple equality
        return isinstance(other, PersistentHeap) and self._data == other._data

    # -------------------
    # Internal Helpers

    def _sift_up(self, data: list[Any], idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if data[idx] < data[parent]:
                data[idx], data[parent] = data[parent], data[idx]
                idx = parent
            else:
                break

    def _sift_down(self, data: list[Any], idx: int) -> None:
        length = len(data)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < length and data[left] < data[smallest]:
                smallest = left
            if right < length and data[right] < data[smallest]:
                smallest = right

            if smallest == idx:
                break

            data[idx], data[smallest] = data[smallest], data[idx]
            idx = smallest
