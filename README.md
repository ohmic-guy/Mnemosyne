# Mnemosyne

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Version](https://img.shields.io/badge/version-0.5.0-orange)
![Tests](https://img.shields.io/badge/tests-108%2F108%20passing-brightgreen)
![Status](https://img.shields.io/badge/status-stable-green)

> **Production-Ready Persistent & Time-Aware Data Structures for Python**

Mnemosyne is a comprehensive Python library implementing **immutable (persistent)** and **time-aware** data structures. Build systems where every operation creates a new version, no data is ever lost, and you can always roll back to any previous state.

**10 fully-typed, battle-tested data structures. 108 comprehensive tests. Zero mutation. Perfect history.**

---

## ✨ Key Features

✅ **Immutable by Design** — Every operation returns a new version; originals never change  
✅ **Structural Sharing** — Efficient memory usage through shared node chains  
✅ **Full Version History** — Access any previous state at O(1) or O(log n) time  
✅ **Time-Aware Variants** — Built-in undo/redo with named checkpoints  
✅ **100% Type-Safe** — Complete type hints for IDE support and type checking  
✅ **Production Grade** — 108 tests, full documentation, Apache 2.0 license  
✅ **Persistent Collections** — Sets, counters, and algebraic operations  

---

## What Are Persistent Data Structures?

Persistent data structures are **immutable**. When you perform an operation, instead of modifying the original, they return a new version. The original remains unchanged.

**Traditional mutable approach:**
```python
stack = []
stack.append(10)  # stack = [10]
stack.append(20)  # stack = [10, 20]
# Original [10] is lost
```

**Persistent approach:**
```python
from mnemosyne.stack import PersistentStack
stack = PersistentStack()
v1 = stack.push(10)  # v1 = [10]
v2 = v1.push(20)     # v2 = [10, 20], v1 still = [10]
# Both versions coexist!
```

**Benefits:**
- No bugs from accidental mutations
- Natural undo/redo implementation
- Concurrent access without locks
- Perfect audit trails
- Easier reasoning about state

---

## Installation

```bash
pip install mnemosyne
```

**Requirements:** Python 3.10+

---

## Quick Start

### 1. Persistent Stack (LIFO)

```python
from mnemosyne.stack import PersistentStack

stack = PersistentStack()
v1 = stack.push(10)
v2 = v1.push(20)
v3 = v2.push(30)

print(v3.to_list())  # [30, 20, 10]
print(v1.to_list())  # [10]  ← Original still exists!

val, v4 = v3.pop()
print(val, v4.to_list())  # 30, [20, 10]
```

### 2. Persistent Queue (FIFO)

```python
from mnemosyne.queue import PersistentQueue

queue = PersistentQueue()
q1 = queue.enqueue(1)
q2 = q1.enqueue(2)
q3 = q2.enqueue(3)

val, q4 = q3.dequeue()
print(val, q4.to_list())  # 1, [2, 3]
```

### 3. Persistent Set with Algebra

```python
from mnemosyne.set import PersistentSet

s1 = PersistentSet().add(1).add(2).add(3)
s2 = PersistentSet().add(2).add(3).add(4)

print(s1.union(s2).to_list())         # [1, 2, 3, 4]
print(s1.intersection(s2).to_list())  # [2, 3]
print(s1.difference(s2).to_list())    # [1]
```

### 4. Persistent Counter (Frequency)

```python
from mnemosyne.counter import PersistentCounter

counter = PersistentCounter()
c1 = counter.increment("apple", 5)
c2 = c1.increment("banana", 3)
c3 = c2.increment("apple", 2)

print(c3.get_count("apple"))     # 7
print(c3.most_common(1))         # [('apple', 7)]
print(c3.total())                # 10
```

### 5. Time-Aware Stack (Undo/Redo)

```python
from mnemosyne.stack import TimeAwareStack

stack = TimeAwareStack()
s1 = stack.push(10)
s2 = s1.push(20)
s3 = s2.push(30)

# Create a checkpoint
s3_checkpoint = s3.checkpoint("before_pop")

s4 = s3.pop()[1]  # Pop 30
print(s4.to_list())  # [20, 10]

# Undo back to checkpoint
s5 = s4.at_checkpoint("before_pop")
print(s5.to_list())  # [30, 20, 10]
```

---

## Data Structures Reference

### Sequences

| Structure | Type | Key Operations | Complexity |
|-----------|------|-----------------|-----------|
| `PersistentStack` | LIFO | push, pop, peek | O(1) |
| `TimeAwareStack` | LIFO + Versioning | + checkpoint, undo, redo | O(1) |
| `PersistentQueue` | FIFO | enqueue, dequeue, peek | O(1) amortized |
| `PersistentDeque` | Double-ended | push_front, push_back, pop_front, pop_back | O(1) |
| `PersistentLinkedList` | Singly-linked | prepend, tail, insert, remove | O(1) prepend, O(k) others |
| `PersistentDoublyLinkedList` | Doubly-linked | append, prepend, pop_front, pop_back, reverse | O(1) ends, O(n) reverse |

### Collections

| Structure | Purpose | Key Operations |
|-----------|---------|-----------------|
| `PersistentSet` | Unique values | add, remove, union, intersection, difference |
| `PersistentCounter` | Frequency tracking | increment, decrement, most_common, total |

### Building Blocks

| Type | Purpose |
|------|---------|
| `SinglyNode` | Foundation for singly-linked structures |
| `DoublyNode` | Foundation for doubly-linked structures |

---

## Architecture & Design

### Structural Sharing

Mnemosyne uses **structural sharing** — when a new version is created, it shares unchanged portions with previous versions instead of copying them.

```
v1: [1] → [2] → [3] → None
         ↗
v2: [0] 
         ↘
          [2] → [3] → None (shared!)
```

This gives us:
- O(1) memory for small changes
- No garbage collection overhead
- Perfect version preservation

### Immutability Guarantee

All data structures are immutable at the API level:
- No `append()` method that modifies — only methods that return new versions
- Safe concurrent access
- No defensive copying needed

### Type Safety

100% type hints using Python's `typing` module:
- IDE autocomplete support
- Static type checking with `mypy`
- Clear parameter and return types
- Optional generic types for flexibility

---

## Use Cases

### 1. **Undo/Redo Systems**
```python
from mnemosyne.stack import TimeAwareStack

editor = TimeAwareStack()
# User types...
editor = editor.push("Hello")
editor = editor.push("Hello World")
editor.checkpoint("document_v1")

# User deletes...
editor = editor.pop()[1]  # Undo = back to previous version!
```

### 2. **Audit Trails**
```python
from mnemosyne.counter import PersistentCounter

events = PersistentCounter()
events = events.increment("login", 1)
events = events.increment("purchase", 1)
events = events.increment("logout", 1)

# Every change is tracked, nothing is lost
```

### 3. **Concurrent Processing**
```python
from mnemosyne.set import PersistentSet

# Multiple threads can safely work on different versions
thread1_set = shared_set.add(1).add(2).add(3)
thread2_set = shared_set.add(4).add(5)
# No locking needed, zero conflicts!
```

### 4. **Exploring State Space**
```python
from mnemosyne.deque import PersistentDeque

initial = PersistentDeque()
branch1 = initial.push_back(1).push_back(2)
branch2 = initial.push_back(3).push_back(4)

# Both branches coexist
print(branch1.to_list())  # [1, 2]
print(branch2.to_list())  # [3, 4]
```

### 5. **Time-Travel Debugging**
```python
from mnemosyne.stack import TimeAwareStack

computation = TimeAwareStack()
for i in range(100):
    computation = computation.push(i)
    computation.checkpoint(f"step_{i}")

# Jump to any point in history
state_at_50 = computation.at_checkpoint("step_50")
```

---

## Testing & Quality

**Test Suite:**
- 108 comprehensive tests
- 100% pass rate
- All data structures fully covered
- Edge cases and error handling validated

**Run Tests:**
```bash
python -m pytest test_mnemosyne.py -v
```

**Test Results:**
```
test_mnemosyne.py::TestPersistentStack ... PASSED
test_mnemosyne.py::TestTimeAwareStack ... PASSED
test_mnemosyne.py::TestPersistentQueue ... PASSED
test_mnemosyne.py::TestPersistentDeque ... PASSED
test_mnemosyne.py::TestPersistentLinkedList ... PASSED
test_mnemosyne.py::TestPersistentDoublyLinkedList ... PASSED
test_mnemosyne.py::TestPersistentSet ... PASSED
test_mnemosyne.py::TestPersistentCounter ... PASSED
test_mnemosyne.py::TestIntegration ... PASSED

======= 108 passed in 0.05s =======
```

---

## Examples

Complete working examples for every data structure:

- [example.py](example.py) — Basic stack operations
- [example_queue.py](example_queue.py) — Queue patterns
- [example_deque_diff.py](example_deque_diff.py) — Deque with versioning
- [example_linkedlist.py](example_linkedlist.py) — Linked list usage
- [example_doublylinkedlist.py](example_doublylinkedlist.py) — Bidirectional list
- [example_set.py](example_set.py) — Set algebra operations
- [example_counter.py](example_counter.py) — Frequency analysis

Run all examples:
```bash
for f in example*.py; do python "$f"; done
```

---

## Performance Characteristics

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Push/Pop (Stack) | O(1) | O(n) with sharing | Constant time |
| Enqueue/Dequeue (Queue) | O(1) amortized | O(n) with sharing | Two-stack model |
| Add/Remove (Set) | O(1) avg | O(n) with sharing | Hash-based bucketing |
| Increment (Counter) | O(1) | O(n) with sharing | Dictionary backed |
| Version Access | O(1) | O(v) where v = versions | Direct reference |

**Memory Efficiency:**
- Small changes: ~1% of original size (structural sharing)
- Large changes: ~100% of new size
- All versions coexist without duplication

---

## API Overview

### Stack Operations
```python
stack = PersistentStack()
stack2 = stack.push(value)      # Returns new stack
val, stack3 = stack2.pop()      # Returns (value, new_stack)
val = stack.peek()              # Peek top without popping
lst = stack.to_list()           # Convert to Python list
```

### Queue Operations
```python
queue = PersistentQueue()
queue2 = queue.enqueue(value)   # Add to back
val, queue3 = queue2.dequeue()  # Remove from front
val = queue.peek()              # Peek front
lst = queue.to_list()           # Convert to list
```

### Set Operations
```python
s1 = PersistentSet()
s2 = s1.add(value)              # Add element
s3 = s2.remove(value)           # Remove element
exists = s1.contains(value)     # Check membership
s4 = s1.union(s2)               # Set union
s5 = s1.intersection(s2)        # Set intersection
s6 = s1.difference(s2)          # Set difference
```

### Counter Operations
```python
counter = PersistentCounter()
c2 = counter.increment(item)                 # Add 1
c3 = c2.decrement(item)                      # Subtract 1
count = c2.get_count(item)                   # Get frequency
c4 = c2.add(other_counter)                   # Combine counters
most = c2.most_common(n)                     # Top n items
```

### Time-Aware Stack
```python
stack = TimeAwareStack()
s2 = stack.push(value)
s2.checkpoint("my_checkpoint")
s3 = stack.pop()[1]
s4 = stack.at_checkpoint("my_checkpoint")    # Jump to checkpoint
versions = stack.all_versions()              # List all versions
```

---

## Contributing

Contributions welcome! Areas for expansion:

- Performance profiling and optimization
- Advanced examples and use cases
- Tree-based structures (BST, Trie, etc.)
- Graph implementations
- Integration examples with popular frameworks

---

## License

Licensed under the **Apache License 2.0** with explicit patent protection.

```
Copyright 2026 Ommkar Ankit Rout

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## Changelog

**v0.5.0** (March 13, 2026)
- Added: `PersistentDoublyLinkedList` with bidirectional operations
- Added: `PersistentSet` with set algebra (union, intersection, difference)
- Added: `PersistentCounter` with frequency analysis and arithmetic
- Changed: License upgraded from MIT to Apache 2.0 (patent protection)
- Tests: 108 comprehensive tests, 100% passing

**v0.4.0** (February 13, 2026)
- Added: `PersistentDeque` with version tracking
- Added: Version diffing for deque structures
- Added: Examples demonstrating diff operations

**v0.1.0 - v0.3.0**
- Foundation: Stack, Queue, LinkedList
- Time-Aware: TimeAwareStack with undo/redo
- Examples and documentation

---

## Questions?

Check the [examples](.) directory for working code for every feature.

Star ⭐ this repo if you find persistent data structures interesting!
