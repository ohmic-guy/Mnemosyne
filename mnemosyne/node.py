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
Immutable node types for persistent linked structures.

Nodes are the fundamental building blocks of persistent data structures.
They support structural sharing, where new structures reuse existing node chains.
"""

from typing import Any, Optional


class SinglyNode:
    """
    Immutable node for singly linked persistent structures.

    Used by:
        - PersistentStack
        - PersistentQueue (two-stack model)
        - PersistentLinkedList (singly)

    Attributes:
        value: The data stored in this node
        next: Reference to the next node, or None if this is the end

    Note:
        Nodes are immutable. Once created, their value cannot change.
        Structural sharing allows multiple data structures to reference the same nodes.
    """

    __slots__ = ("next", "value")

    def __init__(self, value: Any, next: Optional["SinglyNode"] = None) -> None:
        """
        Create a new immutable singly-linked node.

        Args:
            value: The data to store in this node
            next: Reference to the next node (default: None)
        """
        self.value = value
        self.next = next

    def __repr__(self) -> str:
        """Return a string representation of this node."""
        return f"SinglyNode({self.value!r}, next={self.next!r})"


class DoublyNode:
    """
    Immutable node for persistent doubly linked structures.

    Used by:
        - PersistentDoublyLinkedList (future)
        - PersistentDeque (future)

    Attributes:
        value: The data stored in this node
        prev: Reference to the previous node, or None if this is the start
        next: Reference to the next node, or None if this is the end

    Note:
        Nodes are immutable. Once created, their value cannot change.
        Structural sharing allows multiple data structures to reference the same nodes.
    """

    __slots__ = ("next", "prev", "value")

    def __init__(
        self,
        value: Any,
        prev: Optional["DoublyNode"] = None,
        next: Optional["DoublyNode"] = None,
    ) -> None:
        """
        Create a new immutable doubly-linked node.

        Args:
            value: The data to store in this node
            prev: Reference to the previous node (default: None)
            next: Reference to the next node (default: None)
        """
        self.value = value
        self.prev = prev
        self.next = next

    def __repr__(self) -> str:
        """Return a string representation of this node."""
        return f"DoublyNode({self.value!r}, prev={self.prev!r}, next={self.next!r})"
