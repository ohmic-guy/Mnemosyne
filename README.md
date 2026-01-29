# 🧠 Mnemosyne

**Persistent & Time-Aware Data Structures in Python**

Mnemosyne is an open-source Python library that implements persistent (immutable) and time-aware data structures.
Every operation preserves history, enabling inspection, comparison, and navigation of past states without mutation.

The project is built incrementally with an emphasis on clarity, correctness, and structural sharing, inspired by functional data structure design.

## ✨ Key Concepts

**Persistence:**
Operations never overwrite data. Each change produces a new version while old versions remain accessible.

**Time Awareness:**
Explicit version tracking, checkpoints, and undo/redo allow controlled navigation through state history.

**Structural Sharing:**
New versions reuse unchanged parts of old structures for efficiency.

## 📦 Implemented Data Structures

### Persistent Structures

- **PersistentStack**
- **PersistentQueue**
- **PersistentDeque** (Double-Ended Queue)

All persistent structures:
- Are immutable
- Preserve all previous versions
- Support historical inspection

### Time-Aware Structures

- **TimeAwareStack**
  - Version history
  - Named checkpoints
  - Undo / redo
  - Version visualization and diffing

## 🚀 Installation

Currently distributed as source. Clone the repository and import the modules:

```python
from mnemosyne.stack import TimeAwareStack
from mnemosyne.queue import PersistentQueue
from mnemosyne.deque import PersistentDeque
```

## 🔧 Quick Start

### Persistent Deque

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

All versions (v1, v2, v3) remain unchanged.

### Persistent Queue

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

### Time-Aware Stack

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

## 🔍 Version Diffing

Compare changes between two versions:

```python
d.diff(v1, v3)
```

Returns a semantic diff:

```python
{
  "from_version": 1,
  "to_version": 3,
  "added": [...],
  "removed": [...]
}
```

Useful for debugging, auditing, and state inspection.

## 🧠 Design Overview

- Nodes are immutable and linked
- Each operation creates a new version ID
- Old versions are never modified or deleted
- Deque is implemented using two persistent stacks
- Time-aware structures maintain explicit version maps and history stacks

This design aligns with principles from functional programming and persistent data structure research.

## 📁 Project Structure

```
mnemosyne/
│
├── node.py        # Immutable node definition
├── stack.py       # PersistentStack & TimeAwareStack
├── queue.py       # PersistentQueue
├── deque.py       # PersistentDeque
├── __init__.py
│
example.py
example_queue.py
example_deque_diff.py
```

## 🎯 Use Cases

Mnemosyne is suitable for:

- Undo / redo systems
- Time-travel debugging
- Auditable data workflows
- Educational exploration of persistence
- Research and experimentation with immutable structures

## 📌 Project Status

**Current version:** v0.3.x

- Actively developed
- Built incrementally in public

**Planned directions:**
- Shared base abstractions
- Positional and structural diffs
- Persistent trees and graph structures

## 📜 License

This project is released under the MIT License.

## ✍️ Author Note

Mnemosyne is a learning-driven project focused on understanding state, time, and immutability at a deeper level.
The goal is not speed, but correctness and clarity.

---
