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
Persistent min-heap (priority queue) implementations.

A heap is a complete binary tree where every parent is less than or equal to its children.
These implementations keep the underlying array immutable by storing it as a tuple and
creating a new tuple for every operation.
"""

from typing import Any, Iterable


class PersistentHeap:
    """
    Immutable persistent min-heap.

        Architecture:
                - Backed by a tuple representing the heap array (0-based indexing)
                - Original heaps remain untouched; operations create a new tuple reflecting changes
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


class TimeAwareHeap:
    """
    Time-aware min-heap with full version tracking.

    Extends the persistent heap with:
        - Version history tracking (integer version IDs)
        - Named checkpoints
        - Undo/Redo stacks
        - Version diffing

    Architecture:
        _versions: Maps version_id → heap tuple (min-heap array)
        _current_version: The active version ID
        _checkpoints: Maps checkpoint_name → version_id
        _undo_stack: Stack of version IDs for undo
        _redo_stack: Stack of version IDs for redo
    """

    __slots__ = ("_checkpoints", "_current_version", "_redo_stack", "_undo_stack", "_versions")

    def __init__(self) -> None:
        self._versions: dict[int, tuple[Any, ...]] = {0: ()}
        self._current_version: int = 0
        self._checkpoints: dict[str, int] = {}
        self._undo_stack: list[int] = [0]
        self._redo_stack: list[int] = []

    # -------------------
    # Core Operations

    def push(self, value: Any, version: int | None = None) -> int:
        """
        Insert a value into the heap at the given version (default: current).

        Returns:
            The new version ID
        """
        version = self._current_version if version is None else version
        data = list(self._get_version_data(version))
        data.append(value)
        self._sift_up(data, len(data) - 1)

        self._current_version += 1
        self._versions[self._current_version] = tuple(data)
        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()
        return self._current_version

    def pop(self, version: int | None = None) -> tuple[Any, int]:
        """
        Remove and return the smallest value from the heap at the given version.

        Returns:
            (min_value, new_version_id)
        """
        version = self._current_version if version is None else version
        data = list(self._get_version_data(version))

        if not data:
            raise IndexError(f"Pop from empty heap at version {version}")

        min_value = data[0]
        last = data.pop()

        if data:
            data[0] = last
            self._sift_down(data, 0)

        self._current_version += 1
        self._versions[self._current_version] = tuple(data)
        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()
        return min_value, self._current_version

    def peek(self, version: int | None = None) -> Any | None:
        """
        View the smallest element without removing it.

        Returns None if the heap is empty at that version.
        """
        version = self._current_version if version is None else version
        data = self._get_version_data(version)
        return None if not data else data[0]

    # -------------------
    # Version Introspection

    def current_version(self) -> int:
        return self._current_version

    def all_versions(self) -> list[int]:
        return sorted(self._versions.keys())

    def show_version(self, version: int | None = None) -> list[Any]:
        version = self._current_version if version is None else version
        return list(self._get_version_data(version))

    # -------------------
    # Checkpoints

    def checkpoint(self, name: str) -> int:
        if name in self._checkpoints:
            raise ValueError(f"Checkpoint '{name}' already exists")
        self._checkpoints[name] = self._current_version
        return self._current_version

    def jump_to_checkpoint(self, name: str) -> int:
        if name not in self._checkpoints:
            raise KeyError(f"No checkpoint named '{name}'")
        version = self._checkpoints[name]
        self._current_version = version
        self._undo_stack.append(version)
        self._redo_stack.clear()
        return version

    # -------------------
    # Undo / Redo

    def undo(self) -> int:
        if len(self._undo_stack) <= 1:
            raise IndexError("Nothing to undo")
        version = self._undo_stack.pop()
        self._redo_stack.append(version)
        self._current_version = self._undo_stack[-1]
        return self._current_version

    def redo(self) -> int:
        if not self._redo_stack:
            raise IndexError("Nothing to redo")
        version = self._redo_stack.pop()
        self._undo_stack.append(version)
        self._current_version = version
        return version

    # -------------------
    # Diffing

    def diff(self, v1: int, v2: int) -> dict[str, list[Any]]:
        data1 = set(self._get_version_data(v1))
        data2 = set(self._get_version_data(v2))
        return {
            "added": sorted(data2 - data1),
            "removed": sorted(data1 - data2),
        }

    # -------------------
    # Internal Helpers

    def _get_version_data(self, version: int) -> tuple[Any, ...]:
        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")
        return self._versions[version]

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
