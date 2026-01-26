# timelock/stack.py

from .node import Node

class TimeAwareStack:
    """
    A Time-Aware Stack:
    - Each push/pop creates a new version
    - Past versions are immutable and accessible
    - Time is represented by version numbers
    """

    def __init__(self):
        # Dictionary mapping version_id → top Node
        self._versions = {0: None}  
        self._current_version = 0

    def push(self, value, version=None):
        """
        Push a value onto the stack.
        Returns the new version number.
        """
        # Use current version if none specified
        if version is None:
            version = self._current_version

        # Get the top node of the specified version
        top = self._versions[version]

        # Create a new immutable node pointing to previous top
        new_node = Node(value, top)

        # Increment version and store the new top
        self._current_version += 1
        self._versions[self._current_version] = new_node

        return self._current_version

    def pop(self, version=None):
        """
        Pop the top value from the stack.
        Returns a tuple: (popped_value, new_version)
        """
        if version is None:
            version = self._current_version

        top = self._versions[version]

        if top is None:
            raise IndexError("Pop from empty stack")

        # Increment version and move top pointer to previous node
        self._current_version += 1
        self._versions[self._current_version] = top.prev

        return top.value, self._current_version

    def peek(self, version=None):
        """
        Peek at the top value of the stack at a given version.
        Returns None if the stack is empty.
        """
        if version is None:
            version = self._current_version

        top = self._versions[version]
        return None if top is None else top.value

    def current_version(self):
        """
        Returns the current version number.
        """
        return self._current_version