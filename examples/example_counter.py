"""
Example: PersistentCounter

Demonstrates immutable frequency counting and multiset operations.
"""

from mnemosyne.counter import PersistentCounter

# Create an empty counter
c = PersistentCounter()

# Count words from a text
words = ["the", "quick", "brown", "fox", "the", "lazy", "dog", "the"]

counter = c
for word in words:
    counter = counter.increment(word)

print("Word frequencies:")
print(counter.to_dict())
print(f"Total words: {counter.total()}")

# Get most common words
print("\nMost common 3 words:")
for word, count in counter.most_common(3):
    print(f"  {word}: {count}")

# Get least common words
print("\nLeast common 2 words:")
for word, count in counter.least_common(2):
    print(f"  {word}: {count}")

# Counter arithmetic
c1 = PersistentCounter()
c1 = c1.increment("apple", 3)
c1 = c1.increment("banana", 2)

c2 = PersistentCounter()
c2 = c2.increment("apple", 1)
c2 = c2.increment("cherry", 4)

print("\nCounter 1:", c1.to_dict())
print("Counter 2:", c2.to_dict())

c_add = c1 + c2
print("Add (c1 + c2):", c_add.to_dict())

c_sub = c1 - c2
print("Subtract (c1 - c2):", c_sub.to_dict())

# Decrement counts
val, c3 = c1.decrement("apple")
print(f"\nDecremented 'apple' from {val} to {c3.get_count('apple')}")

# Version tracking
print("\nVersion tracking:")
print(f"Initial counter: {c.to_dict()}")
c_v1 = c.increment("a", 5)
print(f"After increment 'a' by 5: {c_v1.to_dict()}")
c_v2 = c_v1.increment("b", 3)
print(f"After increment 'b' by 3: {c_v2.to_dict()}")
val, c_v3 = c_v2.decrement("a", 2)
print(f"After decrement 'a' by 2: {c_v3.to_dict()}")
