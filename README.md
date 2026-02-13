# 🧠 Mnemosyne

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.4.x-orange)
![Status](https://img.shields.io/badge/status-experimental-lightgrey)

> **Persistent & Time-Aware Data Structures in Python**

Mnemosyne is an open-source Python library implementing **immutable (persistent)** and **time-aware** data structures.

Every operation creates a new version.
No mutation. No overwritten history. Full state preservation.

---

## ✨ What It Provides

### 🧩 Core Foundation

* `Node` — Immutable linked-list node
* Linked structural model enabling structural sharing

All higher-level structures are built on this persistent linked foundation.

---

### 🔁 Persistent Structures

* `PersistentStack`
* `PersistentQueue`
* `PersistentDeque`

All structures:

* Are immutable
* Preserve every historical version
* Use structural sharing for efficiency

---

### ⏳ Time-Aware Structures

* `TimeAwareStack`

  * Version tracking
  * Named checkpoints
  * Undo / Redo
  * Version inspection & diffing

---

## 🚀 Example

```python
from mnemosyne.deque import PersistentDeque

d = PersistentDeque()

v1 = d.push_back(10)
v2 = d.push_front(5)

print(d.show_version(v2))  # [5, 10]
```

All previous versions remain accessible.

---

## 🧠 Why Mnemosyne?

* Explore immutable design patterns
* Build undo/redo systems
* Experiment with time-travel debugging
* Learn persistent data structure concepts
* Prototype auditable workflows

---

## 📌 Status

Currently in the **0.x experimental phase**.
APIs may evolve as the architecture matures.

---

## 📜 License

MIT License

---
