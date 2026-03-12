# Mnemosyne

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Version](https://img.shields.io/badge/version-0.5.x-orange)
![Status](https://img.shields.io/badge/status-experimental-lightgrey)

> **Persistent & Time-Aware Data Structures in Python**

Mnemosyne is an open-source Python library implementing **immutable (persistent)** and **time-aware** data structures.

Every operation creates a new version.
No mutation. No overwritten history. Full state preservation.

---

## What It Provides

### Core Foundation

* `Node` — Immutable linked-list node
* Linked structural model enabling structural sharing

All higher-level structures are built on this persistent linked foundation.

---

### Persistent Sequences

* `PersistentStack` — LIFO stack with optional time-awareness
* `PersistentQueue` — FIFO queue via two-stack model
* `PersistentDeque` — Double-ended queue with version tracking
* `PersistentLinkedList` — Singly-linked list structure
* `PersistentDoublyLinkedList` — Bidirectional linked list (append/prepend/pop)

### Persistent Collections

* `PersistentSet` — Hash-based set with set algebra (union, intersection, difference)
* `PersistentCounter` — Frequency counter with arithmetic operations

### All Structures

* Are immutable
* Preserve every historical version
* Use structural sharing for efficiency

---

### Time-Aware Structures

* `TimeAwareStack`

  * Version tracking
  * Named checkpoints
  * Undo / Redo
  * Version inspection & diffing

---

## Examples

**Persistent Deque with versioning:**
```python
from mnemosyne.deque import PersistentDeque

d = PersistentDeque()
v1 = d.push_back(10)
v2 = d.push_front(5)
print(d.show_version(v2))  # [5, 10]
```

**Persistent Set with algebra:**
```python
from mnemosyne.set import PersistentSet

s1 = PersistentSet().add(1).add(2).add(3)
s2 = PersistentSet().add(2).add(3).add(4)
print(s1.intersection(s2))  # {2, 3}
```

**Persistent Counter:**
```python
from mnemosyne.counter import PersistentCounter

c = PersistentCounter()
c = c.increment("apple", 5).increment("banana", 3)
print(c.most_common(1))  # [('apple', 5)]
```

All previous versions remain accessible.

---

## Why Mnemosyne?

* Explore immutable design patterns
* Build undo/redo systems
* Experiment with time-travel debugging
* Learn persistent data structure concepts
* Prototype auditable workflows

---

## Status

Currently in the **0.x experimental phase**.
APIs may evolve as the architecture matures.

---

## License

MIT License

---
