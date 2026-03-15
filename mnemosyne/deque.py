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
Persistent double-ended queue implementation.

A deque (double-ended queue) allows push/pop from both ends.
This implementation uses two TimeAwareStackfor efficient structural sharing.
"""

from typing import Any

from .stack import TimeAwareStack


class PersistentDeque:
    """
    Persistent Double-Ended Queue (Deque).

    Implemented using two Time-Aware Stacks:
        - _front: Stack for elements at the front/left
        - _back: Stack for elements at the back/right

    Each deque version stores a tuple of (front_version, back_version).

    Operations:
        - push_front/push_back: O(1)
        - pop_front/pop_back: O(1) amortized
        - peek_front/peek_back: O(1) amortized

    Example:
        d = PersistentDeque()
        v1 = d.push_back(10)       # [10]
        v2 = d.push_front(5)       # [5, 10]
        v3 = d.push_back(20)       # [5, 10, 20]
        val, v4 = d.pop_front(v3)  # val=5, [10, 20]
    """

    __slots__ = ("_back", "_current_version", "_front", "_versions")

    def __init__(self) -> None:
        """Initialize a persistent deque."""
        self._front = TimeAwareStack()
        self._back = TimeAwareStack()

        self._versions: dict[int, tuple[int, int]] = {0: (0, 0)}
        self._current_version = 0

    # -------------------
    # Internal Utilities

    def _is_stack_empty(self, stack: TimeAwareStack, version: int) -> bool:
        """Check if a stack is empty at a given version."""
        return stack.peek(version) is None

    # -------------------
    # Push Operations

    def push_front(self, value: Any, version: int | None = None) -> int:
        """
        Push a value to the front of the deque.

        Args:
            value: The value to push
            version: Which version to push from (default: current)

        Returns:
            The new version ID

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        new_front_v = self._front.push(value, front_v)

        self._current_version += 1
        self._versions[self._current_version] = (new_front_v, back_v)
        return self._current_version

    def push_back(self, value: Any, version: int | None = None) -> int:
        """
        Push a value to the back of the deque.

        Args:
            value: The value to push
            version: Which version to push from (default: current)

        Returns:
            The new version ID

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        new_back_v = self._back.push(value, back_v)

        self._current_version += 1
        self._versions[self._current_version] = (front_v, new_back_v)
        return self._current_version

    # -------------------
    # Peek Operations

    def peek_front(self, version: int | None = None) -> Any | None:
        """
        View the front element without removing it.

        Args:
            version: Which version to peek (default: current)

        Returns:
            The value at the front, or None if empty

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        if not self._is_stack_empty(self._front, front_v):
            return self._front.peek(front_v)

        back_list = self._back.show_version(back_v)
        return back_list[-1] if back_list else None  # rightmost of back

    def peek_back(self, version: int | None = None) -> Any | None:
        """
        View the back element without removing it.

        Args:
            version: Which version to peek (default: current)

        Returns:
            The value at the back, or None if empty

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        if not self._is_stack_empty(self._back, back_v):
            return self._back.peek(back_v)

        front_list = self._front.show_version(front_v)
        return front_list[-1] if front_list else None  # rightmost of front

    # -------------------
    # Pop Operations

    def pop_front(self, version: int | None = None) -> tuple[Any, int]:
        """
        Pop a value from the front of the deque.

        Args:
            version: Which version to pop from (default: current)

        Returns:
            Tuple of (value, new_version_id)

        Raises:
            IndexError: If deque is empty
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        # Fast path: pop from front stack
        if not self._is_stack_empty(self._front, front_v):
            value, new_front_v = self._front.pop(front_v)

            self._current_version += 1
            self._versions[self._current_version] = (new_front_v, back_v)
            return value, self._current_version

        # Rebalance: move back to front
        back_list = self._back.show_version(back_v)
        if not back_list:
            raise IndexError("Pop from empty deque")

        value = back_list[-1]  # rightmost of back
        remaining = back_list[:-1]  # everything except rightmost

        new_front_v = 0
        for v in remaining:
            new_front_v = self._front.push(v, new_front_v)

        self._current_version += 1
        self._versions[self._current_version] = (new_front_v, 0)

        return value, self._current_version

    def pop_back(self, version: int | None = None) -> tuple[Any, int]:
        """
        Pop a value from the back of the deque.

        Args:
            version: Which version to pop from (default: current)

        Returns:
            Tuple of (value, new_version_id)

        Raises:
            IndexError: If deque is empty
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        # Fast path: pop from back stack
        if not self._is_stack_empty(self._back, back_v):
            value, new_back_v = self._back.pop(back_v)

            self._current_version += 1
            self._versions[self._current_version] = (front_v, new_back_v)
            return value, self._current_version

        # Rebalance: move front to back
        front_list = self._front.show_version(front_v)
        if not front_list:
            raise IndexError("Pop from empty deque")

        value = front_list[-1]  # rightmost of front
        remaining = front_list[:-1]  # everything except rightmost

        new_back_v = 0
        for v in remaining:
            new_back_v = self._back.push(v, new_back_v)

        self._current_version += 1
        self._versions[self._current_version] = (0, new_back_v)

        return value, self._current_version

    # -------------------
    # Utilities

    def show_version(self, version: int | None = None) -> list[Any]:
        """
        Return the deque as a list for a given version.

        Args:
            version: Which version to inspect (default: current)

        Returns:
            List representation of the deque

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        front_v, back_v = self._versions[version]

        front_list = self._front.show_version(front_v)
        back_list = self._back.show_version(back_v)

        return front_list + back_list

    def current_version(self) -> int:
        """Return the current version ID."""
        return self._current_version

    # -------------------
    # Version Difference

    def diff(self, v1: int, v2: int) -> dict[str, Any]:
        """
        Compute semantic difference between two versions.

        This is an order-independent diff (sets, not sequences).

        Args:
            v1: First version ID
            v2: Second version ID

        Returns:
            Dictionary with 'from_version', 'to_version', 'added', 'removed'

        Raises:
            KeyError: If version doesn't exist
        """
        if v1 not in self._versions:
            raise KeyError(f"Version {v1} does not exist")
        if v2 not in self._versions:
            raise KeyError(f"Version {v2} does not exist")

        d1 = self.show_version(v1)
        d2 = self.show_version(v2)

        s1 = set(d1)
        s2 = set(d2)

        return {
            "from_version": v1,
            "to_version": v2,
            "added": list(s2 - s1),
            "removed": list(s1 - s2),
        }

    def __repr__(self) -> str:
        """Return a string representation of this deque."""
        return f"PersistentDeque({self.show_version()!r})"
