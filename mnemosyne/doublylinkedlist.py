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
Persistent doubly-linked list with bidirectional traversal and operations.

A doubly-linked list allows efficient operations from both ends.
This persistent version preserves all historical versions through structural sharing.
"""

from typing import Any

from .node import DoublyNode


class PersistentDoublyLinkedList:
    """
    Immutable persistent doubly linked list.

    Features:
        - All modifying operations return a new list
        - Bidirectional traversal and operations
        - Structural sharing is preserved
        - Efficient append and prepend

    Operations:
        - prepend: O(1), adds to front
        - append: O(1), adds to back
        - pop_front: O(1), removes from front
        - pop_back: O(1), removes from back
        - to_list: O(n), linearizes to Python list

    Example:
        lst = PersistentDoublyLinkedList()
        v1 = lst.append(10)      # [10]
        v2 = lst.append(20)      # [10, 20]
        v3 = lst.prepend(5)      # [5, 10, 20]
        val, v4 = lst.pop_back(v3)  # val=20, [5, 10]
    """

    __slots__ = ("head", "size", "tail")

    def __init__(
        self,
        head: DoublyNode | None = None,
        tail: DoublyNode | None = None,
        size: int = 0,
    ) -> None:
        """
        Initialize a persistent doubly linked list.

        Args:
            head: The head node (internal use)
            tail: The tail node (internal use)
            size: The number of elements (internal use)
        """
        self.head = head
        self.tail = tail
        self.size = size

    # -------------------
    # Basic Utilities

    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self.size == 0

    def __len__(self) -> int:
        """Return the number of elements in the list."""
        return self.size

    def peek_front(self) -> Any:
        """
        Return the first element without removing it.

        Raises:
            IndexError: If the list is empty
        """
        if self.head is None:
            raise IndexError("List is empty")
        return self.head.value

    def peek_back(self) -> Any:
        """
        Return the last element without removing it.

        Raises:
            IndexError: If the list is empty
        """
        if self.tail is None:
            raise IndexError("List is empty")
        return self.tail.value

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

    def prepend(self, value: Any) -> "PersistentDoublyLinkedList":
        """
        Add element to the front of the list (O(1)).

        Args:
            value: The value to prepend

        Returns:
            A new PersistentDoublyLinkedList with the value at the head
        """
        new_head = DoublyNode(value, None, self.head)
        if self.head is not None:
            self.head.prev = new_head
        new_tail = self.tail if self.size > 0 else new_head
        return PersistentDoublyLinkedList(new_head, new_tail, self.size + 1)

    def append(self, value: Any) -> "PersistentDoublyLinkedList":
        """
        Add element to the back of the list (O(1)).

        Args:
            value: The value to append

        Returns:
            A new PersistentDoublyLinkedList with the value at the tail
        """
        new_tail = DoublyNode(value, self.tail, None)
        if self.tail is not None:
            self.tail.next = new_tail
        new_head = self.head if self.size > 0 else new_tail
        return PersistentDoublyLinkedList(new_head, new_tail, self.size + 1)

    def pop_front(self) -> tuple[Any, "PersistentDoublyLinkedList"]:
        """
        Remove the first element (O(1)).

        Returns:
            Tuple of (value, new_list)

        Raises:
            IndexError: If the list is empty
        """
        if self.head is None:
            raise IndexError("List is empty")

        value = self.head.value
        new_head = self.head.next
        if new_head is not None:
            new_head.prev = None
        new_tail = self.tail if self.size > 1 else None

        return value, PersistentDoublyLinkedList(new_head, new_tail, self.size - 1)

    def pop_back(self) -> tuple[Any, "PersistentDoublyLinkedList"]:
        """
        Remove the last element (O(1)).

        Returns:
            Tuple of (value, new_list)

        Raises:
            IndexError: If the list is empty
        """
        if self.tail is None:
            raise IndexError("List is empty")

        value = self.tail.value
        new_tail = self.tail.prev
        if new_tail is not None:
            new_tail.next = None
        new_head = self.head if self.size > 1 else None

        return value, PersistentDoublyLinkedList(new_head, new_tail, self.size - 1)

    def reverse(self) -> "PersistentDoublyLinkedList":
        """
        Return a reversed version of the list (O(n)).

        Returns:
            A new PersistentDoublyLinkedList with elements in reverse order
        """
        result = PersistentDoublyLinkedList()
        current = self.head
        while current:
            result = result.prepend(current.value)
            current = current.next
        return result

    def __repr__(self) -> str:
        """Return a string representation of this doubly linked list."""
        return f"PersistentDoublyLinkedList({self.to_list()!r})"
