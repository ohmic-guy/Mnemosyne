# mnemosyne/node.py

class SinglyNode:
    """
    Immutable node for singly linked persistent structures.
    Used by:
    - PersistentStack
    - PersistentQueue (two-stack model)
    - PersistentLinkedList (singly)
    """

    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class DoublyNode:
    """
    Immutable node for persistent doubly linked structures.
    Used by:
    - PersistentDoublyLinkedList
    - PersistentDeque (future)
    """

    __slots__ = ("value", "prev", "next")

    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next
