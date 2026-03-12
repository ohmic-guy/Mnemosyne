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
Persistent queue implementation using structural sharing.

A queue is a FIFO (First-In-First-Out) data structure.
This implementation uses the two-stack model for efficient persistent queues.
"""

from typing import Any, List, Optional, Tuple
from .stack import PersistentStack


class PersistentQueue:
    """
    Persistent Queue implemented using two persistent stacks.

    Architecture:
        _front: Stack for dequeue operations (LIFO, represents queue front)
        _rear: Stack for enqueue operations (LIFO, represents queue rear)

    When _front is empty, rebalance by reversing _rear into _front.

    Operations:
        - enqueue: O(1)
        - dequeue: O(1) amortized
        - peek: O(1) amortized

    Example:
        q = PersistentQueue()
        q = q.enqueue(10)  # [10]
        q = q.enqueue(20)  # [10, 20]
        val, q = q.dequeue()  # val=10, q=[20]
    """

    __slots__ = ("_front", "_rear")

    def __init__(
        self,
        front: Optional[PersistentStack] = None,
        rear: Optional[PersistentStack] = None,
    ) -> None:
        """
        Initialize a persistent queue.

        Args:
            front: The front stack (internal use)
            rear: The rear stack (internal use)
        """
        self._front = front if front is not None else PersistentStack()
        self._rear = rear if rear is not None else PersistentStack()

    # -------------------
    # Core Operations

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return self._front.is_empty() and self._rear.is_empty()

    def enqueue(self, value: Any) -> "PersistentQueue":
        """
        Add element to the rear of the queue (O(1)).

        Args:
            value: The value to enqueue

        Returns:
            A new PersistentQueue with the value added
        """
        return PersistentQueue(self._front, self._rear.push(value))

    def dequeue(self) -> Tuple[Any, "PersistentQueue"]:
        """
        Remove element from the front of the queue (O(1) amortized).

        Args:
            None

        Returns:
            Tuple of (value, new_queue)

        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        front = self._front
        rear = self._rear

        if front.is_empty():
            # Rebalance: move all from rear to front
            rebalanced = self._rebalance()
            front = rebalanced._front
            rear = rebalanced._rear

        value, new_front = front.pop()
        return value, PersistentQueue(new_front, rear)

    def peek(self) -> Any:
        """
        View the front element without removing it.

        Args:
            None

        Returns:
            The value at the front of the queue

        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")

        front = self._front

        if front.is_empty():
            return self._rebalance().peek()

        return front.peek()

    # -------------------
    # Internal Helper

    def _rebalance(self) -> "PersistentQueue":
        """
        Move all elements from rear to front (reversed order).

        Cost: O(n) but amortized O(1) across operations.

        Returns:
            A new balanced queue
        """
        front = self._front
        rear = self._rear

        while not rear.is_empty():
            value, rear = rear.pop()
            front = front.push(value)

        return PersistentQueue(front, PersistentStack())

    # -------------------
    # Utility

    def to_list(self) -> List[Any]:
        """
        Return queue as a list (front → rear).

        Useful for debugging and verification.

        Returns:
            List representation of the queue
        """
        result: List[Any] = []

        # Collect front stack (from top going down, which is reverse of queue order)
        node = self._front._top
        front_reversed: List[Any] = []
        while node:
            front_reversed.append(node.value)
            node = node.next
        # Reverse to get front in correct order
        result.extend(front_reversed[::-1])

        # Collect rear stack (from top going down, which is reverse of enqueue order)
        node = self._rear._top
        while node:
            result.append(node.value)
            node = node.next

        return result

    def __repr__(self) -> str:
        """Return a string representation of this queue."""
        return f"PersistentQueue({self.to_list()!r})"
