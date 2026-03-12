"""
Example: PersistentDoublyLinkedList

Demonstrates bidirectional operations on a persistent doubly-linked list.
"""

from mnemosyne.doublylinkedlist import PersistentDoublyLinkedList

# Create an empty list
lst = PersistentDoublyLinkedList()

# Append elements to the back
v1 = lst.append(10)
v2 = lst.append(20)
v3 = lst.append(30)

print("After appending [10, 20, 30]:")
print("Version v3:", v3.to_list())

# Prepend elements to the front
v4 = v3.prepend(5)
v5 = v4.prepend(1)

print("\nAfter prepending 1 and 5:")
print("Version v5:", v5.to_list())

# Pop from front and back
val_front, v6 = v5.pop_front()
print(f"\nPopped from front: {val_front}")
print("After pop_front:", v6.to_list())

val_back, v7 = v6.pop_back()
print(f"Popped from back: {val_back}")
print("After pop_back:", v7.to_list())

# Peek without modifying
print(f"\nPeek front: {v5.peek_front()}")
print(f"Peek back: {v5.peek_back()}")

# Reverse the list
v_reversed = v5.reverse()
print(f"\nOriginal: {v5.to_list()}")
print(f"Reversed: {v_reversed.to_list()}")

# All versions remain accessible
print("\nAll versions:")
print(f"v1 (after append 10): {v1.to_list()}")
print(f"v3 (after append 30): {v3.to_list()}")
print(f"v5 (after prepend): {v5.to_list()}")
