"""
VERSION TRACKING BEHAVIOR IN MNEMOSYNE

This document explains how version tracking works across all persistent data structures
in Mnemosyne, with emphasis on TimeAwareStack which provides the most extensive
version management capabilities.

==============================================================================
CORE PRINCIPLE: NO MUTATION, ONLY VERSIONS
==============================================================================

In Mnemosyne, data structures are immutable. Every operation creates a NEW version
instead of modifying the existing structure.

Example:
    stack = PersistentStack()
    v1 = stack.push(10)  # v1 is a new stack with [10]
    v2 = stack.push(20)  # v2 is a new stack with [10, 20]
    # stack remains unchanged: []

This immutability enables:
- Full version history preservation
- Undo/Redo functionality
- Time-travel debugging
- Safe concurrent access (no locks needed)
- Structural sharing for memory efficiency

==============================================================================
VERSION IDS
==============================================================================

Each operation returns a version ID (integer).

In TimeAwareStack:
- Version 0 is the empty stack (always present)
- Version 1 is after the first operation
- Version N is after N operations on that stack instance
- Version IDs are monotonically increasing

Example:
    tas = TimeAwareStack()
    # Current: version 0, stack = []
    
    v1 = tas.push(10)
    # Current: version 1, stack = [10]
    # v0 still accessible: show_version(0) → []
    
    v2 = tas.push(20)
    # Current: version 2, stack = [10, 20]
    # All versions accessible:
    #   show_version(0) → []
    #   show_version(1) → [10]
    #   show_version(2) → [10, 20]

==============================================================================
THE UNDO/REDO STACK
==============================================================================

TimeAwareStack maintains two stacks for undo/redo:

_undo_stack: [0, 1, 2, 3, 4, ...]
             └─ Latest is the current version

_redo_stack: []
             └─ Empty unless you've called undo()

Example 1: Push operations
    tas = TimeAwareStack()
    tas.push(10)   # _undo_stack = [0, 1],    _redo_stack = []
    tas.push(20)   # _undo_stack = [0, 1, 2], _redo_stack = []
    tas.push(30)   # _undo_stack = [0, 1, 2, 3], _redo_stack = []

Example 2: After undo()
    tas.undo()     # _undo_stack = [0, 1, 2], _redo_stack = [3]
    tas.undo()     # _undo_stack = [0, 1],    _redo_stack = [3, 2]

Example 3: After redo()
    tas.redo()     # _undo_stack = [0, 1, 2], _redo_stack = [3]
    tas.redo()     # _undo_stack = [0, 1, 2, 3], _redo_stack = []

Key behavior: When you PUSH after an undo, the redo stack is cleared.
    tas.undo()     # _undo_stack = [0, 1], _redo_stack = [3]
    tas.push(99)   # _undo_stack = [0, 1, 4], _redo_stack = [] (cleared!)
                   # Version 3 is orphaned (inaccessible via undo/redo)
                   # But still accessible via show_version(3)

==============================================================================
CHECKPOINTS
==============================================================================

Checkpoints are named references to versions.

    tas = TimeAwareStack()
    tas.push(10)
    tas.push(20)
    tas.checkpoint("save1")   # Bookmark this version
    
    tas.push(30)
    tas.push(40)
    
    # Later, jump back:
    tas.jump_to_checkpoint("save1")  # Current version = 2 (save1)
    print(tas.show_version(tas.current_version()))  # [10, 20]

Checkpoints are:
- Immutable once created (can't redefine)
- Named (must be unique)
- Useful for "savepoints" in workflows

Error handling:
- Duplicate checkpoint name: ValueError
- Jumping to nonexistent checkpoint: KeyError (with helpful message listing available)

==============================================================================
INDEPENDENT VERSION BRANCHES
==============================================================================

You can create branches by pushing/popping from arbitrary versions.

Example:
    tas = TimeAwareStack()
    v1 = tas.push(10)     # Version 1: [10]
    v2 = tas.push(20)     # Version 2: [10, 20] (current)
    
    # Branch from v1:
    v3 = tas.push(99, version=v1)
    # v3 = Version 3: [10, 99] (branched from v1, not v2)
    
    # All versions exist independently:
    tas.show_version(1)  → [10]
    tas.show_version(2)  → [10, 20]
    tas.show_version(3)  → [10, 99]
    
    # Current version is still 2 (unless you jump)
    tas.current_version()  → 2

This enables workflows where you explore different branches without losing history.

==============================================================================
DIFFING VERSIONS
==============================================================================

Compare any two versions with diff().

    tas = TimeAwareStack()
    v1 = tas.push(10)           # v1 = [10]
    v2 = tas.push(20)           # v2 = [10, 20]
    v3 = tas.push(30)           # v3 = [10, 20, 30]
    val, v4 = tas.pop()         # v4 = [10, 20]
    
    diff = tas.diff(v1, v4)
    # {'added': [20], 'removed': [30]}
    
    diff = tas.diff(v2, v3)
    # {'added': [30], 'removed': []}

Note: Diffs are SET-BASED (order-independent).
If duplicates exist, they're collapsed in the set comparison.

For positional diffs (future feature):
- Track which elements were inserted where
- Track which elements were moved
- Would require additional data structures

==============================================================================
VERSION OPERATIONS IN OTHER STRUCTURES
==============================================================================

PersistentStack:
- Simple immutable stack
- All operations return new PersistentStack instances
- No built-in version tracking or undo/redo
- Can be used as a building block for other structures

PersistentQueue:
- Built from two PersistentStacks
- Operations return new PersistentQueue instances
- No version tracking (use TimeAwareStack variant for time-awareness)

PersistentLinkedList:
- Immutable singly linked list
- All operations return new list instances
- No version tracking

PersistentDeque:
- Built from two TimeAwareStacks
- Each version stores (front_version, back_version) tuple
- Tracks versions of constituent stacks
- Can diff and inspect versions

==============================================================================
ERROR HANDLING AND VALIDATION
==============================================================================

All structures validate inputs and raise meaningful errors:

KeyError exceptions:
- Invalid version ID: "Version X does not exist"
- Invalid checkpoint name: "No checkpoint named 'Y'. Available: [list]"

IndexError exceptions:
- Pop/peek from empty structure: "Pop/peek from empty [structure]"
- Undo with nothing to undo: "Nothing to undo"
- Redo with nothing to redo: "Nothing to redo"

ValueError exceptions:
- Duplicate checkpoint: "Checkpoint 'X' already exists. Use a different name."

IndexError for list/deque operations:
- Insert/remove at invalid index: "Index X out of bounds for [structure]"

==============================================================================
PERFORMANCE NOTES
==============================================================================

Version History Memory:
- Each version is stored in _versions dictionary
- Structural sharing means nodes are shared across versions
- Memory grows with number of versions, but slower than full copies

Undo/Redo Performance:
- O(1) pop from _undo_stack and _redo_stack
- O(1) current_version lookup

Diff Performance:
- O(n) to build list from version (traverse linked structure)
- O(n) set conversion
- O(n) set difference operations
- Overall: O(n) where n = number of elements

Checkpoint Performance:
- O(1) checkpoint creation (dictionary insert)
- O(1) checkpoint lookup and jump

==============================================================================
BEST PRACTICES
==============================================================================

1. Use TimeAwareStack for features like undo/redo and checkpoints
2. Use basic PersistentStack if you don't need time-awareness
3. Checkpoint before major operations
4. Use diff() to audit state changes
5. Version IDs are local to the structure instance (can't compare across instances)
6. Remember: operations don't modify in place, they return new version IDs
7. Store version IDs if you need to reference them later
8. Use show_version(version_id) to inspect historical states

==============================================================================
FUTURE ENHANCEMENTS
==============================================================================

Potential features for version tracking:
- Structural diffing (position-aware, not just set-based)
- Version branching with explicit merge semantics
- Persistent snapshots to disk
- Version tags (like Git)
- Version history visualization
- Time-aware structures for all data types (not just Stack)
"""
