# Copyright 2026 Ommkar Ankit Rout
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Mnemosyne: Persistent & Time-Aware Data Structures

A Python library implementing immutable (persistent) and time-aware data structures.
Every operation creates a new version; no mutation, no overwritten history.

Usage:
    from mnemosyne.stack import PersistentStack, TimeAwareStack
    from mnemosyne.queue import PersistentQueue
    from mnemosyne.deque import PersistentDeque
    from mnemosyne.linkedlist import PersistentLinkedList
    from mnemosyne.doublylinkedlist import PersistentDoublyLinkedList
    from mnemosyne.set import PersistentSet
    from mnemosyne.counter import PersistentCounter
    from mnemosyne.node import SinglyNode, DoublyNode

Core Concept:
    Operations return new versions instead of modifying in place.
    Structural sharing ensures memory efficiency.
    Historical versions remain accessible for undo/redo, diffing, and auditing.
"""

__version__ = "0.5.0"
__author__ = "Mnemosyne Contributors"

from .node import SinglyNode, DoublyNode
from .stack import PersistentStack, TimeAwareStack
from .queue import PersistentQueue
from .deque import PersistentDeque
from .linkedlist import PersistentLinkedList
from .doublylinkedlist import PersistentDoublyLinkedList
from .set import PersistentSet
from .counter import PersistentCounter

__all__ = [
    "SinglyNode",
    "DoublyNode",
    "PersistentStack",
    "TimeAwareStack",
    "PersistentQueue",
    "PersistentDeque",
    "PersistentLinkedList",
    "PersistentDoublyLinkedList",
    "PersistentSet",
    "PersistentCounter",
]
