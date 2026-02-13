from .node import SinglyNode


class PersistentLinkedList:
    """
    Immutable persistent singly linked list.

    - All modifying operations return a new list.
    - Structural sharing is preserved.
    - Only path nodes are copied.
    """

    __slots__ = ("head", "size")

    def __init__(self, head=None, size=0):
        self.head = head
        self.size = size

    # -------------------
    # Basic Utilities

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def peek(self):
        if self.head is None:
            raise IndexError("List is empty")
        return self.head.value

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    # -------------------
    # Core Operations

    def prepend(self, value):
        """
        O(1)
        Copies: 1 node
        """
        new_head = SinglyNode(value, self.head)
        return PersistentLinkedList(new_head, self.size + 1)

    def tail(self):
        """
        Remove first element.
        O(1)
        Copies: 0 nodes
        """
        if self.head is None:
            raise IndexError("List is empty")
        return PersistentLinkedList(self.head.next, self.size - 1)

    def insert(self, index, value):
        """
        Insert at index.
        Copies: index + 1 nodes
        Time: O(index)
        """
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")

        if index == 0:
            return self.prepend(value)

        def clone(node, i):
            if i == 0:
                return SinglyNode(value, node)
            return SinglyNode(node.value, clone(node.next, i - 1))

        new_head = clone(self.head, index)
        return PersistentLinkedList(new_head, self.size + 1)

    def remove(self, index):
        """
        Remove element at index.
        Copies: index nodes
        Time: O(index)
        """
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

        if index == 0:
            return self.tail()

        def clone(node, i):
            if i == 1:
                # skip the removed node
                return SinglyNode(node.value, node.next.next)
            return SinglyNode(node.value, clone(node.next, i - 1))

        new_head = clone(self.head, index)
        return PersistentLinkedList(new_head, self.size - 1)
