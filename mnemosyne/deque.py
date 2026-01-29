# mnemosyne/deque.py

from .stack import TimeAwareStack


class PersistentDeque:
    """
    Persistent Double-Ended Queue (Deque)

    Implemented using two Time-Aware Stacks:
    - front stack
    - back stack

    Each deque version stores:
    (front_stack_version, back_stack_version)
    """

    def __init__(self):
        self._front = TimeAwareStack()
        self._back = TimeAwareStack()

        # deque_version -> (front_version, back_version)
        self._versions = {
            0: (0, 0)
        }
        self._current_version = 0

    # -------------------
    # Push Operations

    def push_front(self, value, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        new_front_v = self._front.push(value, front_v)

        self._current_version += 1
        self._versions[self._current_version] = (new_front_v, back_v)
        return self._current_version

    def push_back(self, value, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        new_back_v = self._back.push(value, back_v)

        self._current_version += 1
        self._versions[self._current_version] = (front_v, new_back_v)
        return self._current_version

    # -------------------
    # Peek Operations

    def peek_front(self, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        val = self._front.peek(front_v)
        if val is not None:
            return val

        # front empty → peek from bottom of back
        back_list = self._back.show_version(back_v)
        return back_list[0] if back_list else None

    def peek_back(self, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        val = self._back.peek(back_v)
        if val is not None:
            return val

        # back empty → peek from bottom of front
        front_list = self._front.show_version(front_v)
        return front_list[0] if front_list else None

    # -------------------
    # Pop Operations

    def pop_front(self, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        if self._front.peek(front_v) is not None:
            value, new_front_v = self._front.pop(front_v)

            self._current_version += 1
            self._versions[self._current_version] = (new_front_v, back_v)
            return value, self._current_version

        # Rebalance from back stack
        back_list = self._back.show_version(back_v)
        if not back_list:
            raise IndexError("Pop from empty deque")

        value = back_list[0]
        remaining = back_list[1:]

        new_front_v = 0
        for v in reversed(remaining):
            new_front_v = self._front.push(v, new_front_v)

        self._current_version += 1
        self._versions[self._current_version] = (new_front_v, 0)
        return value, self._current_version

    def pop_back(self, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        if self._back.peek(back_v) is not None:
            value, new_back_v = self._back.pop(back_v)

            self._current_version += 1
            self._versions[self._current_version] = (front_v, new_back_v)
            return value, self._current_version

        # Rebalance from front stack
        front_list = self._front.show_version(front_v)
        if not front_list:
            raise IndexError("Pop from empty deque")

        value = front_list[0]
        remaining = front_list[1:]

        new_back_v = 0
        for v in reversed(remaining):
            new_back_v = self._back.push(v, new_back_v)

        self._current_version += 1
        self._versions[self._current_version] = (0, new_back_v)
        return value, self._current_version

    # -------------------
    # Utilities

    def show_version(self, version=None):
        version = self._current_version if version is None else version
        front_v, back_v = self._versions[version]

        front_list = self._front.show_version(front_v)
        back_list = self._back.show_version(back_v)

        return front_list + back_list[::-1]

    def current_version(self):
        return self._current_version
    
        # -------------------
    # Version Difference

    def diff(self, v1, v2):
        """
        Show elements added or removed between two deque versions.
        Order-independent semantic diff.
        """
        d1 = self.show_version(v1)
        d2 = self.show_version(v2)

        s1 = set(d1)
        s2 = set(d2)

        added = list(s2 - s1)
        removed = list(s1 - s2)

        return {
            "from_version": v1,
            "to_version": v2,
            "added": added,
            "removed": removed
        }