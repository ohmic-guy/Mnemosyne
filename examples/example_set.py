"""
Example: PersistentSet

Demonstrates immutable set operations with set algebra.
"""

from mnemosyne.set import PersistentSet

# Create an empty set
s = PersistentSet()

# Add elements
s1 = s.add("apple")
s2 = s1.add("banana")
s3 = s2.add("cherry")

print("Set after adding [apple, banana, cherry]:")
print("v3:", s3.to_set())

# Try adding duplicate (ignored)
s4 = s3.add("apple")
print("\nAfter adding 'apple' again:")
print("Same set:", s4 == s3)

# Remove an element
s5 = s3.remove("banana")
print("\nAfter removing 'banana':")
print("v5:", s5.to_set())

# Set operations: Union
s_a = PersistentSet().add(1).add(2).add(3)
s_b = PersistentSet().add(2).add(3).add(4)

print("\nSet A:", s_a.to_set())
print("Set B:", s_b.to_set())

union = s_a.union(s_b)
print("A U B (union):", union.to_set())

intersection = s_a.intersection(s_b)
print("A ∩ B (intersection):", intersection.to_set())

difference = s_a.difference(s_b)
print("A - B (difference):", difference.to_set())

# All versions remain accessible (immutability)
print("\nAll versions:")
print(f"s1: {s1.to_set()}")
print(f"s3: {s3.to_set()}")
print(f"s5: {s5.to_set()}")
