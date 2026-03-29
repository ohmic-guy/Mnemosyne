"""
Example: PersistentHeap (priority queue)

Demonstrates immutable heap operations and structural sharing.
"""

from mnemosyne.heap import PersistentHeap

# Build a heap from scratch
heap = PersistentHeap()
heap = heap.push(5)
heap = heap.push(2)
heap = heap.push(7)
heap = heap.push(1)

print("Min element (peek):", heap.peek())  # 1

# Pop returns (value, new_heap) leaving the old heap intact
val, heap_after_pop = heap.pop()
print("Popped value:", val)  # 1
print("Old heap still starts with:", heap.peek())  # 1
print("New heap starts with:", heap_after_pop.peek())  # 2

# Build from iterable
more = PersistentHeap.from_iterable([9, 3, 6])
combined = heap_after_pop.push(4).push(0)

print("Combined heap values in pop order:")
current = combined
while not current.is_empty():
    v, current = current.pop()
    print(v, end=" ")
print()
