from .node import Node


class PersistentLinkedList:
    __slots__ = ("head", "size")

    def __init__(self, head=None, size=0):
        self.head = head
        self.size = size

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def peek(self):
        if self.head is None:
            raise IndexError("List is empty")
        return self.head.value

    def prepend(self, value):
        new_head = Node(value, self.head)
        return PersistentLinkedList(new_head, self.size + 1)

    def tail(self):
        if self.head is None:
            raise IndexError("List is empty")
        return PersistentLinkedList(self.head.prev, self.size - 1)

    def insert(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Index out of bounds")

        if index == 0:
            return self.prepend(value)

        def clone(node, i):
            if i == 0:
                return Node(value, node)
            return Node(node.value, clone(node.prev, i - 1))

        return PersistentLinkedList(
            clone(self.head, index),
            self.size + 1
        )

    def remove(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")

        if index == 0:
            return self.tail()

        def clone(node, i):
            if i == 1:
                return Node(node.value, node.prev.prev)
            return Node(node.value, clone(node.prev, i - 1))

        return PersistentLinkedList(
            clone(self.head, index),
            self.size - 1
        )

    def to_list(self):
        out = []
        curr = self.head
        while curr:
            out.append(curr.value)
            curr = curr.prev
        return out
