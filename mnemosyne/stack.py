from .node import SinglyNode


class PersistentStack:
    """
    Simple immutable/persistent stack.
    All operations return new stack instances.
    """

    def __init__(self, top=None):
        self._top = top

    def is_empty(self):
        return self._top is None

    def push(self, value):
        new_node = SinglyNode(value, self._top)
        return PersistentStack(new_node)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._top.value, PersistentStack(self._top.next)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._top.value


class TimeAwareStack:
    """
    Time-Aware Stack with full features:
    - Immutable versions of the stack
    - Version history tracking
    - Named checkpoints
    - Undo / Redo
    - Version difference and visualization
    """

    def __init__(self):
        self._versions = {0: None}        # version_id -> top SinglyNode
        self._current_version = 0
        self._checkpoints = {}            # name -> version_id
        self._undo_stack = [0]            # initialize with base version
        self._redo_stack = []

    # -------------------
    # Core Operations

    def push(self, value, version=None):
        version = self._current_version if version is None else version
        top = self._versions[version]
        new_node = SinglyNode(value, top)

        self._current_version += 1
        self._versions[self._current_version] = new_node

        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()

        return self._current_version

    def pop(self, version=None):
        version = self._current_version if version is None else version
        top = self._versions[version]

        if top is None:
            raise IndexError("Pop from empty stack")

        self._current_version += 1
        self._versions[self._current_version] = top.next

        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()

        return top.value, self._current_version

    def peek(self, version=None):
        version = self._current_version if version is None else version
        top = self._versions.get(version)
        return None if top is None else top.value

    def current_version(self):
        return self._current_version

    # -------------------
    # Version Utilities

    def show_version(self, version):
        """Return stack as list for a given version"""
        node = self._versions.get(version)
        result = []

        while node:
            result.append(node.value)
            node = node.next

        return result[::-1]  # bottom → top

    def all_versions(self):
        return list(self._versions.keys())

    def checkpoint(self, name):
        self._checkpoints[name] = self._current_version

    def jump_to_checkpoint(self, name):
        if name not in self._checkpoints:
            raise KeyError(f"No checkpoint named '{name}'")
        self._current_version = self._checkpoints[name]

    # -------------------
    # Undo / Redo

    def undo(self):
        if len(self._undo_stack) < 2:
            raise IndexError("Nothing to undo")

        last = self._undo_stack.pop()
        self._redo_stack.append(last)
        self._current_version = self._undo_stack[-1]

        return self._current_version

    def redo(self):
        if not self._redo_stack:
            raise IndexError("Nothing to redo")

        next_version = self._redo_stack.pop()
        self._undo_stack.append(next_version)
        self._current_version = next_version

        return self._current_version

    # -------------------
    # Version Difference

    def diff(self, v1, v2):
        s1 = set(self.show_version(v1))
        s2 = set(self.show_version(v2))

        added = s2 - s1
        removed = s1 - s2

        return {"added": list(added), "removed": list(removed)}

    # -------------------
    # Visualization

    def visualize(self, version=None):
        version = self._current_version if version is None else version
        stack_list = self.show_version(version)

        print(f"Stack (bottom → top) [version {version}]:")
        print("---")
        for val in stack_list:
            print(val)
        print("---")
