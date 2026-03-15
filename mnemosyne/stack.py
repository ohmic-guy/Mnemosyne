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
Persistent stack implementations with time-awareness support.

A stack is a LIFO (Last-In-First-Out) data structure.
Persistent stacks preserve all historical versions through structural sharing.
"""

from typing import Any

from .node import SinglyNode


class PersistentStack:
    """
    Simple immutable/persistent stack (LIFO).

    All operations return new stack instances.
    Historical versions remain accessible.

    Structure:
        Stack is represented as a linked list of SinglyNode objects.
        Each push creates a new node and a new PersistentStack instance.
        Structural sharing reuses the previous node chain.

    Operations are O(1) for push, pop, and peek.

    Example:
        stack = PersistentStack()
        v1 = stack.push(10)      # [10]
        v2 = stack.push(20)      # [10, 20]
        val, v3 = stack.pop()    # val=20, stack=[10]
    """

    __slots__ = ("_top",)

    def __init__(self, top: SinglyNode | None = None) -> None:
        """
        Initialize a persistent stack.

        Args:
            top: The topmost node of the stack (internal use)
        """
        self._top = top

    def is_empty(self) -> bool:
        """Check if the stack is empty."""
        return self._top is None

    def push(self, value: Any) -> "PersistentStack":
        """
        Push a value onto the stack.

        Args:
            value: The value to push

        Returns:
            A new PersistentStack with the value on top
        """
        new_node = SinglyNode(value, self._top)
        return PersistentStack(new_node)

    def pop(self) -> tuple[Any, "PersistentStack"]:
        """
        Pop a value from the stack.

        Args:
            None

        Returns:
            Tuple of (value, new_stack)
            value is the popped element
            new_stack is the stack with the top element removed

        Raises:
            IndexError: If the stack is empty
        """
        if self._top is None:
            raise IndexError("pop from empty stack")
        return self._top.value, PersistentStack(self._top.next)

    def peek(self) -> Any:
        """
        View the top element without removing it.

        Returns:
            The value at the top of the stack

        Raises:
            IndexError: If the stack is empty
        """
        if self._top is None:
            raise IndexError("peek from empty stack")
        return self._top.value

    def __repr__(self) -> str:
        """Return a string representation of this stack."""
        items = []
        node = self._top
        while node:
            items.append(node.value)
            node = node.next
        return f"PersistentStack({items[::-1]!r})"


class TimeAwareStack:
    """
    Time-Aware Stack with full version tracking features.

    Extends PersistentStack with:
        - Version history tracking
        - Named checkpoints
        - Undo/Redo operations
        - Version diffing and visualization

    Structure:
        _versions: Maps version_id → SinglyNode (internal state)
        _current_version: The active version ID
        _checkpoints: Maps checkpoint_name → version_id
        _undo_stack: Stack of operations for undo
        _redo_stack: Stack of operations for redo

    Example:
        tas = TimeAwareStack()
        v1 = tas.push(10)
        v2 = tas.push(20)
        tas.checkpoint("saved")
        v3, _ = tas.pop()
        tas.undo()  # Back to v2
    """

    __slots__ = ("_checkpoints", "_current_version", "_redo_stack", "_undo_stack", "_versions")

    def __init__(self) -> None:
        """Initialize a time-aware stack."""
        self._versions: dict[int, SinglyNode | None] = {0: None}
        self._current_version: int = 0
        self._checkpoints: dict[str, int] = {}
        self._undo_stack: list[int] = [0]
        self._redo_stack: list[int] = []

    # -------------------
    # Core Operations

    def push(self, value: Any, version: int | None = None) -> int:
        """
        Push a value onto the stack at a given version (or current).

        Args:
            value: The value to push
            version: Which version to push from (default: current version)

        Returns:
            The new version ID

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        top = self._versions[version]
        new_node = SinglyNode(value, top)

        self._current_version += 1
        self._versions[self._current_version] = new_node

        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()

        return self._current_version

    def pop(self, version: int | None = None) -> tuple[Any, int]:
        """
        Pop a value from the stack at a given version (or current).

        Args:
            version: Which version to pop from (default: current version)

        Returns:
            Tuple of (value, new_version_id)

        Raises:
            IndexError: If the stack is empty at that version
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        top = self._versions[version]

        if top is None:
            raise IndexError(f"Pop from empty stack at version {version}")

        self._current_version += 1
        self._versions[self._current_version] = top.next

        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()

        return top.value, self._current_version

    def peek(self, version: int | None = None) -> Any | None:
        """
        View the top element without removing it.

        Args:
            version: Which version to peek into (default: current version)

        Returns:
            The value at the top of the stack, or None if empty

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        top = self._versions.get(version)
        return None if top is None else top.value

    def current_version(self) -> int:
        """Return the current version ID."""
        return self._current_version

    # -------------------
    # Version Utilities

    def show_version(self, version: int) -> list[Any]:
        """
        Return stack as a list for a given version.

        Args:
            version: The version to inspect

        Returns:
            List representation of the stack (bottom → top)

        Raises:
            KeyError: If version doesn't exist
        """
        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        node = self._versions.get(version)
        result = []

        while node:
            result.append(node.value)
            node = node.next

        return result[::-1]  # bottom → top

    def all_versions(self) -> list[int]:
        """Return a sorted list of all version IDs."""
        return sorted(self._versions.keys())

    def checkpoint(self, name: str) -> None:
        """
        Create a named checkpoint at the current version.

        Args:
            name: Unique name for this checkpoint

        Raises:
            ValueError: If checkpoint name already exists
        """
        if name in self._checkpoints:
            raise ValueError(f"Checkpoint '{name}' already exists. Use a different name.")
        self._checkpoints[name] = self._current_version

    def jump_to_checkpoint(self, name: str) -> int:
        """
        Jump the current version to a named checkpoint.

        Args:
            name: The checkpoint name

        Returns:
            The version ID of the checkpoint

        Raises:
            KeyError: If checkpoint doesn't exist
        """
        if name not in self._checkpoints:
            avail = list(self._checkpoints.keys())
            raise KeyError(f"No checkpoint named '{name}'. Available: {avail}")
        self._current_version = self._checkpoints[name]
        return self._current_version

    # -------------------
    # Undo / Redo

    def undo(self) -> int:
        """
        Undo the last operation.

        Returns:
            The new (previous) version ID

        Raises:
            IndexError: If there's nothing to undo
        """
        if len(self._undo_stack) < 2:
            raise IndexError("Nothing to undo")

        last = self._undo_stack.pop()
        self._redo_stack.append(last)
        self._current_version = self._undo_stack[-1]

        return self._current_version

    def redo(self) -> int:
        """
        Redo the last undone operation.

        Returns:
            The new (forward) version ID

        Raises:
            IndexError: If there's nothing to redo
        """
        if not self._redo_stack:
            raise IndexError("Nothing to redo")

        next_version = self._redo_stack.pop()
        self._undo_stack.append(next_version)
        self._current_version = next_version

        return self._current_version

    # -------------------
    # Version Difference

    def diff(self, v1: int, v2: int) -> dict[str, list[Any]]:
        """
        Compute semantic difference between two versions.

        This is an order-independent diff (sets, not sequences).
        For ordered differences, see future structural diffing.

        Args:
            v1: First version ID
            v2: Second version ID

        Returns:
            Dictionary with 'added' and 'removed' keys

        Raises:
            KeyError: If version doesn't exist
        """
        if v1 not in self._versions:
            raise KeyError(f"Version {v1} does not exist")
        if v2 not in self._versions:
            raise KeyError(f"Version {v2} does not exist")

        s1: set[Any] = set(self.show_version(v1))
        s2: set[Any] = set(self.show_version(v2))

        added = s2 - s1
        removed = s1 - s2

        return {"added": list(added), "removed": list(removed)}

    # -------------------
    # Visualization

    def visualize(self, version: int | None = None) -> None:
        """
        Print a visual representation of the stack.

        Args:
            version: Which version to visualize (default: current)

        Raises:
            KeyError: If version doesn't exist
        """
        version = self._current_version if version is None else version

        if version not in self._versions:
            raise KeyError(f"Version {version} does not exist")

        stack_list = self.show_version(version)

        print(f"Stack (bottom → top) [version {version}]:")
        print("---")
        for val in stack_list:
            print(val)
        print("---")

    def __repr__(self) -> str:
        """Return a string representation of this time-aware stack."""
        return (
            f"TimeAwareStack("
            f"current_version={self._current_version}, "
            f"versions={len(self._versions)}, "
            f"checkpoints={list(self._checkpoints.keys())})"
        )
