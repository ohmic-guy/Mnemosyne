# Copyright 2026 Ommkar Ankit Rout
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Persistent counter for tracking occurrences of values.

Similar to Python's collections.Counter, but immutable and persistent.
Useful for frequency analysis, histograms, and multisets.
"""

from typing import Any, Dict, List, Optional, Tuple


class PersistentCounter:
    """
    Immutable persistent counter that tracks value occurrences.

    Features:
        - Counts elements in an immutable way
        - All operations return new counter instances
        - Supports arithmetic operations (add, subtract)
        - Efficient O(1) increment/decrement

    operations:
        - increment: O(1), adds to count
        - decrement: O(1), subtracts from count
        - get_count: O(1), gets count for value
        - most_common: O(n log n), sorted by frequency

    Example:
        c = PersistentCounter()
        c1 = c.increment("apple")        # {"apple": 1}
        c2 = c1.increment("apple")       # {"apple": 2}
        c3 = c2.increment("orange")      # {"apple": 2, "orange": 1}
        val, c4 = c3.decrement("apple")  # val=2, {"apple": 1, "orange": 1}
    """

    __slots__ = ("_counts",)

    def __init__(self, counts: Optional[Dict[Any, int]] = None) -> None:
        """
        Initialize a persistent counter.

        Args:
            counts: Internal counts dictionary (internal use)
        """
        self._counts = counts if counts is not None else {}

    # -------------------
    # Basic Utilities

    def is_empty(self) -> bool:
        """Check if the counter is empty."""
        return len(self._counts) == 0

    def __len__(self) -> int:
        """Return the number of unique values."""
        return len(self._counts)

    def get_count(self, value: Any) -> int:
        """
        Get the count for a value.

        Args:
            value: The value to look up

        Returns:
            The count (0 if not present)
        """
        return self._counts.get(value, 0)

    def total(self) -> int:
        """
        Get the total count across all values.

        Returns:
            Sum of all counts
        """
        return sum(self._counts.values())

    def to_dict(self) -> Dict[Any, int]:
        """
        Convert to a Python dictionary.

        Returns:
            A dictionary of value -> count
        """
        return dict(self._counts)

    def to_list(self) -> List[Tuple[Any, int]]:
        """
        Convert to a list of (value, count) tuples.

        Returns:
            List of (value, count) pairs in arbitrary order
        """
        return list(self._counts.items())

    # -------------------
    # Core Operations

    def increment(self, value: Any, amount: int = 1) -> "PersistentCounter":
        """
        Increment the count for a value (O(1)).

        Args:
            value: The value to increment
            amount: How much to increment by (default: 1)

        Returns:
            A new PersistentCounter with the incremented value

        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")

        new_counts = self._counts.copy()
        new_counts[value] = new_counts.get(value, 0) + amount
        return PersistentCounter(new_counts)

    def decrement(
        self, value: Any, amount: int = 1
    ) -> Tuple[int, "PersistentCounter"]:
        """
        Decrement the count for a value (O(1)).

        Args:
            value: The value to decrement
            amount: How much to decrement by (default: 1)

        Returns:
            Tuple of (old_count, new_counter)
            If count reaches 0, the value is removed

        Raises:
            ValueError: If amount is not positive or exceeds current count
            KeyError: If value is not in counter
        """
        if amount <= 0:
            raise ValueError(f"Amount must be positive, got {amount}")

        if value not in self._counts:
            raise KeyError(f"Value {value!r} not in counter")

        old_count = self._counts[value]
        
        if old_count < amount:
            raise ValueError(
                f"Cannot decrement {value!r} by {amount}: "
                f"current count is {old_count}"
            )

        new_counts = self._counts.copy()

        if old_count <= amount:
            del new_counts[value]
        else:
            new_counts[value] = old_count - amount

        return old_count, PersistentCounter(new_counts)

    def most_common(self, n: Optional[int] = None) -> List[Tuple[Any, int]]:
        """
        Return the most common values and their counts.

        Args:
            n: How many top values to return (default: all)

        Returns:
            List of (value, count) pairs sorted by count descending
        """
        sorted_items = sorted(
            self._counts.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_items if n is None else sorted_items[:n]

    def least_common(self, n: Optional[int] = None) -> List[Tuple[Any, int]]:
        """
        Return the least common values and their counts.

        Args:
            n: How many bottom values to return (default: all)

        Returns:
            List of (value, count) pairs sorted by count ascending
        """
        sorted_items = sorted(self._counts.items(), key=lambda x: x[1])
        return sorted_items if n is None else sorted_items[:n]

    def add(self, other: "PersistentCounter") -> "PersistentCounter":
        """
        Add counts from another counter.

        Args:
            other: Another PersistentCounter

        Returns:
            A new PersistentCounter with combined counts
        """
        new_counts = self._counts.copy()
        for value, count in other._counts.items():
            new_counts[value] = new_counts.get(value, 0) + count
        return PersistentCounter(new_counts)

    def subtract(self, other: "PersistentCounter") -> "PersistentCounter":
        """
        Subtract counts from another counter.

        Negative counts are removed from the result.

        Args:
            other: Another PersistentCounter

        Returns:
            A new PersistentCounter with subtracted counts
        """
        new_counts = self._counts.copy()
        for value, count in other._counts.items():
            if value in new_counts:
                new_counts[value] -= count
                if new_counts[value] <= 0:
                    del new_counts[value]
        return PersistentCounter(new_counts)

    def __repr__(self) -> str:
        """Return a string representation of this counter."""
        return f"PersistentCounter({self.to_dict()!r})"

    def __eq__(self, other: Any) -> bool:
        """Check equality with another counter."""
        if not isinstance(other, PersistentCounter):
            return False
        return self._counts == other._counts

    def __add__(self, other: "PersistentCounter") -> "PersistentCounter":
        """Support + operator for addition."""
        return self.add(other)

    def __sub__(self, other: "PersistentCounter") -> "PersistentCounter":
        """Support - operator for subtraction."""
        return self.subtract(other)
