# mnemosyne/queue.py

from .stack import PersistentStack

class PersistentQueue:
    def __init__(self, front=None, rear=None):
        self._front = front or PersistentStack()
        self._rear = rear or PersistentStack()

    def is_empty(self):
        return self._front.is_empty() and self._rear.is_empty()

    def enqueue(self, value):
        # enqueue goes to rear stack
        return PersistentQueue(self._front, self._rear.push(value))

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")

        # If front is empty, rebalance
        if self._front.is_empty():
            return self._rebalance().dequeue()

        value, new_front = self._front.pop()
        return value, PersistentQueue(new_front, self._rear)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")

        if self._front.is_empty():
            return self._rebalance().peek()

        value, _ = self._front.pop()
        return value

    def _rebalance(self):
        """
        Move all elements from rear to front (reversed order).
        """
        front = self._front
        rear = self._rear

        while not rear.is_empty():
            value, rear = rear.pop()
            front = front.push(value)

        return PersistentQueue(front, PersistentStack())