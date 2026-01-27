# Changelog

All notable changes to this project will be documented in this file.

The format follows common open-source conventions and aims to keep changes
clear, explicit, and easy to track.

---

## [0.1.0] - 2026-01-26

### Added
- Initial public release of **Mnemosyne**
- PersistentStack data structure
- Immutable versioned stack operations:
  - push
  - pop
  - peek
- Full access to historical versions
- Named checkpoints
- Undo and redo support
- Version comparison utilities
- Simple stack visualization
- MIT License
- Project documentation (README)

### Notes
- This is an experimental release focused on correctness and clarity
- API is subject to change while the project is in 0.x versions
- Additional persistent data structures are planned

---

## [0.2.0] - 2026-01-27

### Added
- **PersistentStack**: Simple immutable stack implementation
  - Fully persistent with structural sharing
  - Core operations: push, pop, peek, is_empty
  - All operations return new stack instances
- **PersistentQueue**: Immutable queue using two-stack implementation
  - Efficient amortized O(1) operations
  - Maintains immutability across enqueue/dequeue
  - Automatic rebalancing when front stack is empty
  - Core operations: enqueue, dequeue, peek, is_empty
- Example code for PersistentQueue (example_queue.py)

### Changed
- Refactored stack.py to include both PersistentStack and TimeAwareStack
- TimeAwareStack now coexists with simpler PersistentStack implementation

---

## [Unreleased]

### Planned
- Improved version graph / branching timelines for TimeAwareStack
- Expanded test coverage
- Additional persistent data structures (deque, trees)
- API refinements based on usage