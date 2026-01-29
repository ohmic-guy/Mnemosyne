# Changelog

All notable changes to Mnemosyne are documented in this file.

The format follows semantic versioning and emphasizes clarity, correctness, and incremental progress.

---

## [0.3.0] - 2026-01-30

### Added
- **PersistentDeque**: Double-ended queue implementation
  - Fully persistent with structural sharing
  - Implemented using two persistent stacks (front and back)
  - Core operations: `push_front`, `push_back`, `pop_front`, `pop_back`
  - All operations return new version IDs
  - Historical version preservation and inspection
- **Version Diffing**: Semantic diff between any two versions
  - `diff(v1, v2)` method for PersistentDeque
  - Returns structured output showing added/removed elements
  - Useful for debugging, auditing, and state inspection
- Example code demonstrating deque and diffing (`example_deque_diff.py`)

### Changed
- Updated README with modern formatting and emoji section headers
- Reorganized documentation to emphasize key concepts upfront
- Added comprehensive Design Overview section
- Included Project Status and roadmap

### Notes
- This release focuses on extending the persistent structure family
- Version diffing capabilities demonstrate practical use of version history
- API remains stable but subject to refinement in 0.x series

---

## [0.2.0] - 2026-01-27

### Added
- **PersistentStack**: Simple immutable stack implementation
  - Fully persistent with structural sharing
  - Core operations: `push`, `pop`, `peek`, `is_empty`
  - All operations return new stack instances
- **PersistentQueue**: Immutable queue using two-stack implementation
  - Efficient amortized O(1) operations
  - Maintains immutability across enqueue/dequeue
  - Automatic rebalancing when front stack is empty
  - Core operations: `enqueue`, `dequeue`, `peek`, `is_empty`
- Example code for PersistentQueue (`example_queue.py`)

### Changed
- Refactored `stack.py` to include both PersistentStack and TimeAwareStack
- TimeAwareStack now coexists with simpler PersistentStack implementation
- Improved structural sharing across persistent structures

---

## [0.1.0] - 2026-01-26

### Added
- Initial public release of **Mnemosyne**
- **TimeAwareStack**: Versioned stack with time-travel capabilities
  - Immutable versioned operations: `push`, `pop`, `peek`
  - Full access to historical versions via `show_version`
  - Named checkpoints with `checkpoint` and `jump_to_checkpoint`
  - Undo and redo support
  - Version comparison utilities
  - Stack state visualization
- Immutable **Node** class for linked-list structure
- MIT License
- Comprehensive README documentation
- Example code demonstrating time-aware operations (`example.py`)

### Notes
- Experimental release focused on correctness and clarity over performance
- API is subject to change while the project is in 0.x versions
- Foundation for additional persistent data structures

---

## [Unreleased]

### Planned
- Shared base abstractions for all persistent structures
- Positional and structural diffs
- Persistent trees (BST, AVL)
- Persistent graph structures
- Enhanced version graph visualization
- Branching timelines for TimeAwareStack
- Expanded test coverage and benchmarks
- API refinements based on usage patterns