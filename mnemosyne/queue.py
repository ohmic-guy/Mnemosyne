from .stack import PersistentStack


class PersistentQueue:
    """
    Persistent Queue implemented using two persistent stacks.

    _front: stack for dequeue operations
    _rear:  stack for enqueue operations

    When _front is empty, we rebalance by reversing _rear into _front.
    """

    def __init__(self, front=None, rear=None):
        self._front = front if front is not None else PersistentStack()
        self._rear = rear if rear is not None else PersistentStack()

    # -------------------
    # Core Operations

    def is_empty(self):
        return self._front.is_empty() and self._rear.is_empty()

    def enqueue(self, value):
        """
        Add element to the queue.
        O(1)
        """
        return PersistentQueue(self._front, self._rear.push(value))

    def dequeue(self):
        """
        Remove element from queue.
        Amortized O(1)
        """
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        front = self._front
        rear = self._rear

        if front.is_empty():
            # Rebalance first
            rebalanced = self._rebalance()
            front = rebalanced._front
            rear = rebalanced._rear

        value, new_front = front.pop()
        return value, PersistentQueue(new_front, rear)

    def peek(self):
        """
        View front element without removing it.
        """
        if self.is_empty():
            raise IndexError("peek from empty queue")

        front = self._front

        if front.is_empty():
            return self._rebalance().peek()

        return front.peek()

    # -------------------
    # Internal Helper

    def _rebalance(self):
        """
        Move all elements from rear to front (reversed order).
        Cost: O(n) but amortized O(1) across operations.
        """
        front = self._front
        rear = self._rear

        while not rear.is_empty():
            value, rear = rear.pop()
            front = front.push(value)

        return PersistentQueue(front, PersistentStack())

    # -------------------
    # Utility

    def to_list(self):
        """
        Return queue as a list (front → rear).
        Useful for debugging.
        """
        # Get front elements (already in correct order)
        front_list = self._front.show_version(0) if False else None
        # We can't access internals of stack easily,
        # so rebuild manually

        result = []

        # Collect front (bottom → top)
        node = self._front._top
        temp = []
        while node:
            temp.append(node.value)
            node = node.next
        result.extend(temp[::-1])

        # Collect rear (top → bottom, but must append in correct order)
        node = self._rear._top
        while node:
            result.append(node.value)
            node = node.next

        return result
