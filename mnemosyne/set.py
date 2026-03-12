"""
Persistent set implementation using structural sharing.

A set is an unordered collection of unique values.
This persistent implementation maintains immutability and version history.
"""

from typing import Any, List, Optional, Set as PySet
from .linkedlist import PersistentLinkedList
from .node import SinglyNode


class PersistentSet:
    """
    Immutable persistent set using hash bucketing with linked lists.

    Architecture:
        - Hash table of persistent linked lists (for collision handling)
        - Structural sharing preserves memory efficiency
        - All operations return new set instances

    Operations:
        - add: O(1) average, O(n) worst case (collision)
        - remove: O(1) average, O(n) worst case
        - contains: O(1) average, O(n) worst case
        - to_set: O(n), converts to Python set

    Example:
        s = PersistentSet()
        s1 = s.add(10)      # {10}
        s2 = s1.add(20)     # {10, 20}
        s3 = s2.add(10)     # {10, 20} (10 already exists)
        s4 = s3.remove(10)  # {20}
    """

    __slots__ = ("_buckets", "_size", "_bucket_count")

    def __init__(
        self,
        buckets: Optional[List[Optional[PersistentLinkedList]]] = None,
        size: int = 0,
        bucket_count: int = 16,
    ) -> None:
        """
        Initialize a persistent set.

        Args:
            buckets: Internal bucket array (internal use)
            size: Number of unique elements
            bucket_count: Number of hash buckets
        """
        if buckets is None:
            buckets = [None] * bucket_count

        self._buckets = buckets
        self._size = size
        self._bucket_count = bucket_count

    # -------------------
    # Basic Utilities

    def is_empty(self) -> bool:
        """Check if the set is empty."""
        return self._size == 0

    def __len__(self) -> int:
        """Return the number of unique elements."""
        return self._size

    def _hash(self, value: Any) -> int:
        """Compute hash bucket index for a value."""
        try:
            return hash(value) % self._bucket_count
        except TypeError:
            # Unhashable type, use id
            return id(value) % self._bucket_count

    def contains(self, value: Any) -> bool:
        """
        Check if value is in the set.

        Args:
            value: The value to check

        Returns:
            True if value is in the set, False otherwise
        """
        bucket_idx = self._hash(value)
        bucket = self._buckets[bucket_idx]

        if bucket is None:
            return False

        # Search in the linked list
        for v in bucket.to_list():
            if v == value:
                return True
        return False

    def __contains__(self, value: Any) -> bool:
        """Support 'in' operator."""
        return self.contains(value)

    def to_set(self) -> PySet[Any]:
        """
        Convert to a Python set.

        Returns:
            A Python set with all elements
        """
        result: PySet[Any] = set()
        for bucket in self._buckets:
            if bucket is not None:
                for value in bucket.to_list():
                    result.add(value)
        return result

    def to_list(self) -> List[Any]:
        """
        Convert to a Python list (unordered).

        Returns:
            A list with all elements
        """
        return list(self.to_set())

    # -------------------
    # Core Operations

    def add(self, value: Any) -> "PersistentSet":
        """
        Add a value to the set (O(1) average).

        Args:
            value: The value to add

        Returns:
            A new PersistentSet with the value added
            (unchanged if value already exists)
        """
        if self.contains(value):
            return self

        bucket_idx = self._hash(value)
        bucket = self._buckets[bucket_idx]

        # Create new bucket with the value
        if bucket is None:
            new_bucket = PersistentLinkedList().prepend(value)
        else:
            new_bucket = bucket.prepend(value)

        # Create new buckets array
        new_buckets = self._buckets[:]
        new_buckets[bucket_idx] = new_bucket

        return PersistentSet(new_buckets, self._size + 1, self._bucket_count)

    def remove(self, value: Any) -> "PersistentSet":
        """
        Remove a value from the set (O(1) average).

        Args:
            value: The value to remove

        Returns:
            A new PersistentSet without the value

        Raises:
            KeyError: If value is not in the set
        """
        if not self.contains(value):
            raise KeyError(f"Value {value!r} not in set")

        bucket_idx = self._hash(value)
        bucket = self._buckets[bucket_idx]

        assert bucket is not None

        # Remove from linked list
        items = bucket.to_list()
        new_bucket_list = [v for v in items if v != value]

        # Create new buckets array
        new_buckets = self._buckets[:]
        if not new_bucket_list:
            new_buckets[bucket_idx] = None
        else:
            # Rebuild list from items
            new_bucket = PersistentLinkedList()
            for v in reversed(new_bucket_list):
                new_bucket = new_bucket.prepend(v)
            new_buckets[bucket_idx] = new_bucket

        return PersistentSet(new_buckets, self._size - 1, self._bucket_count)

    # -------------------
    # Set Operations

    def union(self, other: "PersistentSet") -> "PersistentSet":
        """
        Return the union of this set and another.

        Args:
            other: Another PersistentSet

        Returns:
            A new PersistentSet with elements from both sets
        """
        result = self
        for value in other.to_list():
            result = result.add(value)
        return result

    def intersection(self, other: "PersistentSet") -> "PersistentSet":
        """
        Return the intersection of this set and another.

        Args:
            other: Another PersistentSet

        Returns:
            A new PersistentSet with elements in both sets
        """
        result = PersistentSet()
        for value in self.to_list():
            if other.contains(value):
                result = result.add(value)
        return result

    def difference(self, other: "PersistentSet") -> "PersistentSet":
        """
        Return the difference of this set and another.

        Args:
            other: Another PersistentSet

        Returns:
            A new PersistentSet with elements in this but not other
        """
        result = self
        for value in other.to_list():
            if result.contains(value):
                result = result.remove(value)
        return result

    def __repr__(self) -> str:
        """Return a string representation of this set."""
        return f"PersistentSet({self.to_set()!r})"

    def __eq__(self, other: Any) -> bool:
        """Check equality with another set."""
        if not isinstance(other, PersistentSet):
            return False
        return self.to_set() == other.to_set()
