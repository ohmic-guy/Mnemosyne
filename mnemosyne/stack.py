# mnemosyne/stack.py

from .node import Node

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
        self._versions = {0: None}        # version_id -> top Node
        self._current_version = 0
        self._checkpoints = {}            # name -> version_id
        self._undo_stack = []             # for undo
        self._redo_stack = []             # for redo

    # Core Operations
    def push(self, value, version=None):
        version = self._current_version if version is None else version
        top = self._versions[version]
        new_node = Node(value, top)

        self._current_version += 1
        self._versions[self._current_version] = new_node

        # Track undo/redo
        self._undo_stack.append(self._current_version)
        self._redo_stack.clear()

        return self._current_version

    def pop(self, version=None):
        version = self._current_version if version is None else version
        top = self._versions[version]
        if top is None:
            raise IndexError("Pop from empty stack")

        self._current_version += 1
        self._versions[self._current_version] = top.prev

        # Track undo/redo
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
            node = node.prev
        return result[::-1]

    def all_versions(self):
        """List all version numbers"""
        return list(self._versions.keys())

    def checkpoint(self, name):
        """Assign a name to current version"""
        self._checkpoints[name] = self._current_version

    def jump_to_checkpoint(self, name):
        """Set current version to named checkpoint"""
        if name not in self._checkpoints:
            raise KeyError(f"No checkpoint named '{name}'")
        self._current_version = self._checkpoints[name]

    # -------------------
    # Undo / Redo
    def undo(self):
        if len(self._undo_stack) < 2:
            raise IndexError("Nothing to undo")
        last = self._undo_stack.pop()       # remove current
        self._redo_stack.append(last)       # save for redo
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
        """Show elements added or removed between two versions"""
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
        print("Stack (bottom → top) [version {}]:".format(version))
        print("---")
        for val in stack_list:
            print(val)
        print("---")