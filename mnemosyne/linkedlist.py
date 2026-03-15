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
Persistent linked list implementation with structural sharing.

A linked list is a linear data structure accessed through pointers.
Persistent linked lists preserve all historical versions through structural sharing.
"""

from typing import Any

from .node import SinglyNode


class PersistentLinkedList:
    """
    Immutable persistent singly linked list.

    Features:
        - All modifying operations return a new list
        - Structural sharing is preserved
        - Only path nodes are copied (O(index) for insertions)
        - Full version history maintained

    Operations:
        - prepend: O(1), copies 1 node
        - tail: O(1), copies 0 nodes
        - insert: O(index), copies (index+1) nodes
        - remove: O(index), copies index nodes
        - peek: O(1)

    Example:
        lst = PersistentLinkedList()
        v1 = lst.prepend(10)      # [10]
        v2 = v1.prepend(20)       # [20, 10]
        v3 = v2.insert(1, 15)     # [20, 15, 10]
    """

    __slots__ = ("head", "size")

    def __init__(self, head: SinglyNode | None = None, size: int = 0) -> None:
        """
        Initialize a persistent linked list.

        Args:
            head: The head node (internal use)
            size: The number of elements (internal use)
        """
        self.head = head
        self.size = size

    # -------------------
    # Basic Utilities

    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self.size == 0

    def __len__(self) -> int:
        """Return the number of elements in the list."""
        return self.size

    def peek(self) -> Any:
        """
        Return the first element without removing it.

        Returns:
            The value at the head of the list

        Raises:
            IndexError: If the list is empty
        """
        if self.head is None:
            raise IndexError("List is empty")
        return self.head.value

    def to_list(self) -> list[Any]:
        """
        Convert the persistent list to a Python list.

        Returns:
            A list of all values in order
        """
        result: list[Any] = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    # -------------------
    # Core Operations

    def prepend(self, value: Any) -> "PersistentLinkedList":
        """
        Add element to the front of the list (O(1)).

        Args:
            value: The value to prepend

        Returns:
            A new PersistentLinkedList with the value at the head

        Note:
            Copies: 1 node
        """
        new_head = SinglyNode(value, self.head)
        return PersistentLinkedList(new_head, self.size + 1)

    def tail(self) -> "PersistentLinkedList":
        """
        Remove the first element (O(1)).

        Returns:
            A new PersistentLinkedList without the head element

        Raises:
            IndexError: If the list is empty

        Note:
            Copies: 0 nodes (pure structural sharing)
        """
        if self.head is None:
            raise IndexError("List is empty")
        return PersistentLinkedList(self.head.next, self.size - 1)

    def insert(self, index: int, value: Any) -> "PersistentLinkedList":
        """
        Insert a value at a specific index (O(index)).

        Args:
            index: The position to insert (0 = front)
            value: The value to insert

        Returns:
            A new PersistentLinkedList with the value inserted

        Raises:
            IndexError: If index is out of bounds

        Note:
            Copies: index + 1 nodes
        """
        if index < 0 or index > self.size:
            raise IndexError(f"Index {index} out of bounds for list of size {self.size}")

        if index == 0:
            return self.prepend(value)

        def clone(node: SinglyNode | None, i: int) -> SinglyNode:
            """Recursively clone nodes until insertion point."""
            if i == 0:
                return SinglyNode(value, node)
            assert node is not None  # Type safety
            return SinglyNode(node.value, clone(node.next, i - 1))

        new_head = clone(self.head, index)
        return PersistentLinkedList(new_head, self.size + 1)

    def remove(self, index: int) -> "PersistentLinkedList":
        """
        Remove element at a specific index (O(index)).

        Args:
            index: The position to remove (0 = head)

        Returns:
            A new PersistentLinkedList without the element at index

        Raises:
            IndexError: If index is out of bounds

        Note:
            Copies: index nodes
        """
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of bounds for list of size {self.size}")

        if index == 0:
            return self.tail()

        def clone(node: SinglyNode | None, i: int) -> SinglyNode:
            """Recursively clone nodes until removal point."""
            if i == 1:
                # Skip the removed node
                assert node is not None  # Type safety
                assert node.next is not None  # Type safety
                return SinglyNode(node.value, node.next.next)
            assert node is not None  # Type safety
            return SinglyNode(node.value, clone(node.next, i - 1))

        new_head = clone(self.head, index)
        return PersistentLinkedList(new_head, self.size - 1)

    def __repr__(self) -> str:
        """Return a string representation of this linked list."""
        return f"PersistentLinkedList({self.to_list()!r})"
