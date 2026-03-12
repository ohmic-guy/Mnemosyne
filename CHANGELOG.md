# Changelog

All notable changes to **Mnemosyne** are documented in this file.

The project follows **Semantic Versioning** (`MAJOR.MINOR.PATCH`).
While in the `0.x` series, APIs may evolve as the architecture matures.

---

## [0.5.0] - 2026-03-13

### Added

#### New Data Structures

**PersistentDoublyLinkedList**
* Bidirectional linked list enabling efficient front/back operations
* Operations:
  * `append` — Add element at end (O(1))
  * `prepend` — Add element at start (O(1))
  * `pop_front` — Remove from start (O(1))
  * `pop_back` — Remove from end (O(1))
  * `peek_front` / `peek_back` — View without removing
  * `reverse` — Create reversed copy (O(n))
* Full version preservation and structural sharing

**PersistentSet**
* Hash-based immutable set with set algebra
* Operations:
  * `add`, `remove`, `contains` — Core membership
  * `union` — Combine both sets
  * `intersection` — Common elements only
  * `difference` — Elements in first set only
* 16-bucket hash table with collision chaining via linked lists
* Full version preservation

**PersistentCounter**
* Immutable frequency counter (multiset)
* Operations:
  * `increment(item, amount)` — Increase frequency
  * `decrement(item, amount)` — Decrease frequency (validates count >= amount)
  * `get_count(item)` — Query frequency
  * `total()` — Sum of all counts
  * `most_common(n)` / `least_common(n)` — Frequency analysis
  * `add(other)` / `subtract(other)` — Arithmetic with operators
* Full version preservation
* Input validation on all operations

#### Examples

* `example_doublylinkedlist.py` — Bidirectional list operations
* `example_set.py` — Set algebra and membership testing
* `example_counter.py` — Frequency counting and analysis

#### Test Coverage

* 42 new tests across 3 test classes
* Total test suite: 108 comprehensive tests
* 100% pass rate

### Changed

* Version updated: 0.4.0 → 0.5.0
* `__init__.py` exports expanded from 7 to 10 data structures

---

## [0.4.0] - 2026-02-13

### Added

#### PersistentDeque

* Fully persistent double-ended queue
* Implemented using two persistent stacks (front/back model)
* Structural sharing across all versions
* Operations:

  * `push_front`
  * `push_back`
  * `pop_front`
  * `pop_back`
* All operations return new version IDs
* Complete historical version preservation

#### Version Diffing

* `diff(v1, v2)` for PersistentDeque
* Structured semantic diff output

  * Added elements
  * Removed elements
* Enables debugging, auditing, and state inspection
* Foundation for future structural and positional diffing

#### Examples

* `example_deque_diff.py` demonstrating:

  * Version creation
  * State transitions
  * Cross-version comparison

---

## [0.3.0] - 2026-01-30

### Added

#### PersistentDeque (Initial Release)

* Double-ended immutable structure
* Built from two persistent stacks
* Amortized efficient operations
* Version-aware design compatible with Mnemosyne philosophy

### Documentation

* Modernized README formatting
* Emoji-based section headers
* Design Overview section
* Project Status and roadmap
* Clear emphasis on structural sharing

---

## [0.2.0] - 2026-01-27

### Added

#### PersistentStack

* Immutable stack with structural sharing
* Operations:

  * `push`
  * `pop`
  * `peek`
  * `is_empty`
* All operations return new stack instances

#### PersistentQueue

* Immutable queue via two-stack implementation
* Amortized O(1) enqueue/dequeue
* Automatic rebalancing
* Operations:

  * `enqueue`
  * `dequeue`
  * `peek`
  * `is_empty`

#### Examples

* `example_queue.py`

### Changed

* Refactored `stack.py`:

  * Coexistence of `PersistentStack` and `TimeAwareStack`
* Improved internal structural sharing
* Cleaner separation of responsibilities between stack variants

---

## [0.1.0] - 2026-01-26

### Initial Release

#### TimeAwareStack

* Versioned immutable stack
* Time-travel capabilities:

  * `push`
  * `pop`
  * `peek`
* Historical inspection via `show_version`
* Named checkpoints:

  * `checkpoint`
  * `jump_to_checkpoint`
* Undo/redo support
* Version comparison utilities
* Stack visualization

#### Core Architecture

* Immutable `Node` class (linked-list backbone)
* Structural sharing foundation
* MIT License
* Comprehensive README
* `example.py` demonstrating time-aware operations

### Philosophy

* Correctness over performance
* Clarity over abstraction
* Explicit versioning as a first-class concept

---

## [Unreleased]

### Planned

#### Architecture

* Shared base abstractions for persistent structures
* Unified version graph model
* Branching timelines for TimeAwareStack

#### Data Structures

* Persistent Binary Search Tree
* Persistent AVL Tree
* Persistent graph structures

#### Tooling

* Positional and structural diffing
* Enhanced version graph visualization
* Expanded test coverage
* Benchmarks
* API refinement based on real usage

---