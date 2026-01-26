# timelock/node.py

class Node:
    __slots__ = ("value", "prev")

    def __init__(self, value, prev):
        self.value = value
        self.prev = prev