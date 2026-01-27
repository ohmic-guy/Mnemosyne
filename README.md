# Mnemosyne: Persistent & Time-Aware Data Structures

A Python library for persistent and time-aware data structures. Mnemosyne provides:
- **Persistent structures** (PersistentStack, PersistentQueue) with full immutability and structural sharing
- **Time-aware structures** (TimeAwareStack) with versioning, checkpoints, and undo/redo capabilities

All data structures maintain immutability, allowing you to preserve and access previous states.

## Features

### Persistent Data Structures
- **PersistentStack**: Immutable stack with structural sharing
- **PersistentQueue**: Efficient immutable queue using two-stack implementation
- All operations return new instances, preserving old versions

### Time-Aware Structures
- **Immutable Versions**: Every operation creates a new immutable version
- **Version History**: Access and inspect any previous version
- **Named Checkpoints**: Save important states with meaningful names
- **Undo/Redo**: Navigate backward and forward through your operation history
- **Version Visualization**: View all versions and their state at a glance

## Installation

Clone the repository and import the modules:

```python
# For persistent structures
from mnemosyne.stack import PersistentStack
from mnemosyne.queue import PersistentQueue

# For time-aware structures
from mnemosyne.stack import TimeAwareStack
```

## Quick Start

### Persistent Queue

```python
from mnemosyne.queue import PersistentQueue

# Create a new queue
q0 = PersistentQueue()
q1 = q0.enqueue(10)
q2 = q1.enqueue(20)
q3 = q2.enqueue(30)

# Dequeue preserves old versions
val, q4 = q3.dequeue()  # val = 10

# Old versions still work
print(q1.peek())  # 10 - q1 is unchanged!
```

### Persistent Stack

```python
from mnemosyne.stack import PersistentStack

# Create a new stack
s0 = PersistentStack()
s1 = s0.push(10)
s2 = s1.push(20)

# Pop returns value and new stack
val, s3 = s2.pop()  # val = 20

# Old versions remain intact
print(s1.peek())  # 10
```

### Time-Aware Stack

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

### PersistentStack

#### `push(value) -> PersistentStack`
Returns a new stack with the value pushed on top.

```python
s1 = s0.push(42)
```

#### `pop() -> tuple[any, PersistentStack]`
Returns (value, new_stack) tuple.

```python
val, s1 = s0.pop()
```

#### `peek() -> any`
Returns the top value without modifying the stack.

#### `is_empty() -> bool`
Returns True if the stack is empty.

### PersistentQueue

#### `enqueue(value) -> PersistentQueue`
Returns a new queue with the value added to the rear.

```python
q1 = q0.enqueue(42)
```

#### `dequeue() -> tuple[any, PersistentQueue]`
Returns (value, new_queue) tuple.

```python
val, q1 = q0.dequeue()
```

#### `peek() -> any`
Returns the front value without removing it.

#### `is_empty() -> bool`
Returns True if the queue is empty.

### TimeAwareStack - Core Operations

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
  stack.py         # PersistentStack and TimeAwareStack implementations
  queue.py         # PersistentQueue implementation
example.py         # TimeAwareStack usage examples
example_queue.py   # PersistentQueue usage examples
```

## Running the Examples

```bash
# Run time-aware stack example
python3 example.py

# Run persistent queue example
python3 example_queue.py
```

## Author Notes

Mnemosyne provides a clean, functional approach to stack operations with complete history preservation. Use it when you need to explore alternative paths through your data without losing the original path.
