# Mnemosyne

> **Persistent & Time-Aware Data Structures in Python**

Mnemosyne is an open-source Python library implementing **persistent (immutable)** and **time-aware** data structures.

Every operation produces a new version.
No mutation. No overwritten history. Full state preservation.

The project is built incrementally with an emphasis on:

* Correctness over performance
* Structural sharing over copying
* Explicit versioning over implicit mutation
* Clarity over abstraction

Inspired by functional data structure design and research on persistence.

---

# Core Ideas

## Persistence

Operations never modify existing data.

Each change:

* Creates a new version
* Preserves all previous versions
* Reuses unchanged structure via structural sharing

You can inspect *any past state* at any time.

---

## Time Awareness

Some structures explicitly track history and navigation:

* Version IDs
* Named checkpoints
* Undo / Redo
* Version comparison
* State visualization

Time becomes a first-class concept.

---

## Structural Sharing

New versions reuse unchanged nodes instead of copying entire structures.

This keeps:

* Memory usage efficient
* Version creation fast
* History scalable

---

# Implemented Structures

## Persistent Structures

All persistent structures:

* Are immutable
* Preserve historical versions
* Support version inspection

### • PersistentStack

Simple immutable stack.

### • PersistentQueue

Two-stack implementation with amortized O(1) operations.

### • PersistentDeque

Double-ended queue implemented using two persistent stacks.

Supports:

* `push_front`
* `push_back`
* `pop_front`
* `pop_back`
* `diff(v1, v2)`

---

## Time-Aware Structures

### • TimeAwareStack

Adds explicit time navigation on top of persistence:

* Version history tracking
* Named checkpoints
* Undo / Redo
* Version comparison
* State inspection

---

# Installation

Currently distributed as source.

```bash
git clone https://github.com/ohmic-guy/Mnemosyne.git
cd Mnemosyne
```

Import directly:

```python
from mnemosyne.stack import TimeAwareStack
from mnemosyne.queue import PersistentQueue
from mnemosyne.deque import PersistentDeque
```

---

# Quick Start

## Persistent Deque

```python
from mnemosyne.deque import PersistentDeque

d = PersistentDeque()

v1 = d.push_back(10)
v2 = d.push_front(5)
v3 = d.push_back(20)

print(d.show_version(v3))   # [5, 10, 20]

val, v4 = d.pop_front(v3)

print(val)                  # 5
print(d.show_version(v4))   # [10, 20]
```

All previous versions (`v1`, `v2`, `v3`) remain unchanged.

---

## Persistent Queue

```python
from mnemosyne.queue import PersistentQueue

q = PersistentQueue()

v1 = q.enqueue(10)
v2 = q.enqueue(20)
v3 = q.enqueue(30)

val, v4 = q.dequeue(v3)

print(val)                  # 10
print(q.show_version(v2))   # [10, 20]
```

---

## Time-Aware Stack

```python
from mnemosyne.stack import TimeAwareStack

s = TimeAwareStack()

v1 = s.push(10)
v2 = s.push(20)
v3 = s.push(30)

s.checkpoint("before_pop")

val, v4 = s.pop(v3)

print(s.show_version(v2))   # [10, 20]

s.jump_to_checkpoint("before_pop")
s.undo()
s.redo()
```

---

# Version Diffing

Compare two versions:

```python
d.diff(v1, v3)
```

Returns:

```python
{
  "from_version": 1,
  "to_version": 3,
  "added": [...],
  "removed": [...]
}
```

Useful for:

* Debugging
* Auditing state changes
* Educational inspection
* Time-travel workflows

---

# Design Overview

* Nodes are immutable
* Structures are linked
* Each operation generates a new version ID
* Old versions are never modified or deleted
* Deque uses two persistent stacks
* Time-aware structures maintain explicit version maps and history stacks

The architecture prioritizes conceptual clarity over micro-optimization.

---

# Project Structure

```
mnemosyne/
│
├── node.py        # Immutable node
├── stack.py       # PersistentStack & TimeAwareStack
├── queue.py       # PersistentQueue
├── deque.py       # PersistentDeque
├── __init__.py
│
example.py
example_queue.py
example_deque_diff.py
```

---

# Use Cases

Mnemosyne is ideal for:

* Undo / Redo systems
* Time-travel debugging tools
* Auditable workflows
* Event-sourced systems
* Educational exploration of immutability
* Research on persistent structures

---

# Project Status

**Current Version:** v0.4.x
**Stability:** Experimental but stable within 0.x guarantees

While in the `0.x` series:

* APIs may evolve
* Internal architecture may refine
* Focus remains on correctness and clarity

---

# Roadmap

* Shared base abstractions for persistent structures
* Positional and structural diffing
* Branching timelines
* Persistent trees (BST, AVL)
* Persistent graph structures
* Version graph visualization
* Expanded tests and benchmarks

---

# License

MIT License.

---

# Author Note

Mnemosyne is a learning-driven project exploring state, time, and immutability at a deeper level.

The goal is not raw performance —
but conceptual integrity, structural clarity, and architectural correctness.
---