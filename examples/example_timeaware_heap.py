"""
Example: TimeAwareHeap (versioned priority queue)

Demonstrates immutable heap operations with undo/redo and checkpoints.
"""

from mnemosyne.heap import TimeAwareHeap

heap = TimeAwareHeap()

v1 = heap.push(5)
v2 = heap.push(2)
v3 = heap.push(7)

print("Versions:", heap.all_versions())  # [0, 1, 2, 3]
print("Current min:", heap.peek())       # 2

# Checkpoint current state
heap.checkpoint("initial_three")

# Pop creates a new version
val, v4 = heap.pop()
print("Popped:", val)                     # 2
print("After pop version:", v4)
print("Min after pop:", heap.peek(v4))     # 5

# Undo/redo navigation
heap.undo()
print("After undo, version:", heap.current_version())
print("Min after undo:", heap.peek())

heap.redo()
print("After redo, version:", heap.current_version())
print("Min after redo:", heap.peek())

# Diff two versions
print("Diff between v2 and v4:", heap.diff(v2, v4))
