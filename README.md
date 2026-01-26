# Mnemosyne: Time-Aware Data Structures

A Python library for building time-aware data structures. It ships with a stack implementation initially, and the same versioning, checkpoint, and undo/redo core can be reused for queues, deques, trees, or any structure where you want time-travel semantics.

## Features

- **Immutable Versions**: Every operation creates a new immutable version
- **Version History**: Access and inspect any previous version
- **Named Checkpoints**: Save important states with meaningful names
- **Undo/Redo**: Navigate backward and forward through your operation history
- **Version Visualization**: View all versions and their state at a glance

## Installation

Clone the repository and import the module:

```python
from mnemosyne.stack import TimeAwareStack
```

## Quick Start

```python
from mnemosyne.stack import TimeAwareStack

# Create a new time-aware stack
s = TimeAwareStack()

# Push values and capture version IDs
v1 = s.push(10)
v2 = s.push(20)
v3 = s.push(30)

# Create a named checkpoint
s.checkpoint("before_pop")

# Pop a value
val, v4 = s.pop(v3)

# View all versions
print(s.all_versions())  # [0, 1, 2, 3, 4]

# Show stack state at a specific version
print(s.show_version(v2))  # [10, 20]

# Jump back to a checkpoint
s.jump_to_checkpoint("before_pop")

# Undo and redo operations
s.undo()
s.redo()
```

## API Reference

### Core Operations

#### `push(value, version=None) -> int`
Push a value onto the stack. Returns the new version ID.

```python
v = s.push(42)
```

#### `pop(version=None) -> tuple`
Pop a value from the stack. Returns (value, new_version_id).

```python
val, v = s.pop()
```

#### `peek(version=None) -> any`
Peek at the top value without removing it.

```python
top = s.peek()
```

### Version Management

#### `current_version() -> int`
Get the current version ID.

#### `all_versions() -> list`
Get a list of all version IDs.

#### `show_version(version) -> list`
Get the complete stack state as a list for a given version.

```python
stack_state = s.show_version(v1)
```

#### `checkpoint(name: str)`
Create a named checkpoint at the current version.

```python
s.checkpoint("important_state")
```

#### `jump_to_checkpoint(name: str)`
Jump to a previously saved checkpoint.

```python
s.jump_to_checkpoint("important_state")
```

### Undo/Redo

#### `undo() -> int`
Undo the last operation. Returns the new current version ID.

#### `redo() -> int`
Redo the last undone operation. Returns the new current version ID.

## How It Works

Mnemosyne uses a **linked-list node structure** to maintain immutable versions:

- Each stack state is represented as a chain of `Node` objects
- Every push/pop operation creates a new version ID
- Version history is preserved, allowing non-destructive time travel
- Checkpoints provide semantic bookmarks in your history

## Extending to Other Data Structures

The core version-tracking pattern works for queues, deques, trees, and more:
- Define how a node/state references the previous state (or children) immutably.
- Implement operations (enqueue, dequeue, insert, delete, etc.) so each returns a new top/root reference and version ID.
- Reuse the existing bookkeeping: `self._versions`, `self._current_version`, `_undo_stack`, `_redo_stack`, and checkpoints.
- Expose helpers like `show_version` tailored to your structure (e.g., breadth-first for trees).

## Example Use Case

Perfect for applications that need:
- **Collaborative editing** with version tracking
- **Undo/redo functionality** in data manipulation tools
- **Debugging** by rewinding and replaying operations
- **Time-series analysis** where you need snapshots at different points

## File Structure

```
mnemosyne/
  __init.py__      # Package initialization
  node.py          # Node class for linked-list structure
  stack.py         # TimeAwareStack implementation
example.py         # Usage examples
```

## Running the Example

```bash
python3 example.py
```

## Author Notes

Mnemosyne provides a clean, functional approach to stack operations with complete history preservation. Use it when you need to explore alternative paths through your data without losing the original path.
