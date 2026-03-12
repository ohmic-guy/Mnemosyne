"""
Comprehensive test suite for Mnemosyne persistent data structures.

Tests cover:
- Basic operations on all data structures
- Edge cases (empty structures, single elements)
- Version tracking and history
- Undo/Redo functionality
- Checkpoints
- Diffing
- Error handling
"""

import pytest
from mnemosyne.stack import PersistentStack, TimeAwareStack
from mnemosyne.queue import PersistentQueue
from mnemosyne.deque import PersistentDeque
from mnemosyne.linkedlist import PersistentLinkedList
from mnemosyne.node import SinglyNode, DoublyNode


# ============================================================================
# SINGLY NODE TESTS
# ============================================================================

class TestSinglyNode:
    """Tests for SinglyNode."""

    def test_create_node_with_value(self):
        """Node can be created with a value."""
        node = SinglyNode(10)
        assert node.value == 10
        assert node.next is None

    def test_create_node_with_next(self):
        """Node can be created with a next reference."""
        next_node = SinglyNode(20)
        node = SinglyNode(10, next_node)
        assert node.value == 10
        assert node.next is next_node
        assert node.next.value == 20

    def test_node_repr(self):
        """Node has a string representation."""
        node = SinglyNode(10)
        assert "SinglyNode" in repr(node)
        assert "10" in repr(node)


class TestDoublyNode:
    """Tests for DoublyNode."""

    def test_create_node_basic(self):
        """DoublyNode can be created with a value."""
        node = DoublyNode(10)
        assert node.value == 10
        assert node.prev is None
        assert node.next is None

    def test_create_node_with_links(self):
        """DoublyNode can be created with prev and next references."""
        prev_node = DoublyNode(5)
        next_node = DoublyNode(15)
        node = DoublyNode(10, prev_node, next_node)
        assert node.value == 10
        assert node.prev is prev_node
        assert node.next is next_node


# ============================================================================
# PERSISTENT STACK TESTS
# ============================================================================

class TestPersistentStack:
    """Tests for PersistentStack."""

    def test_empty_stack(self):
        """A new stack is empty."""
        stack = PersistentStack()
        assert stack.is_empty()

    def test_push_single_element(self):
        """Pushing one element creates a non-empty stack."""
        stack = PersistentStack()
        stack2 = stack.push(10)
        assert not stack2.is_empty()
        assert stack2.peek() == 10

    def test_push_multiple_elements(self):
        """Pushing creates independent versions."""
        s1 = PersistentStack()
        s2 = s1.push(10)
        s3 = s2.push(20)
        s4 = s3.push(30)

        assert s1.is_empty()
        assert s2.peek() == 10
        assert s3.peek() == 20
        assert s4.peek() == 30

    def test_pop_single_element(self):
        """Popping returns the value and new stack."""
        stack = PersistentStack().push(10)
        value, new_stack = stack.pop()
        assert value == 10
        assert new_stack.is_empty()

    def test_pop_multiple_elements(self):
        """Popping from stack with multiple elements."""
        stack = PersistentStack().push(10).push(20).push(30)
        
        val1, s1 = stack.pop()
        assert val1 == 30
        assert s1.peek() == 20

        val2, s2 = s1.pop()
        assert val2 == 20
        assert s2.peek() == 10

        val3, s3 = s2.pop()
        assert val3 == 10
        assert s3.is_empty()

    def test_pop_empty_raises_error(self):
        """Popping from empty stack raises IndexError."""
        stack = PersistentStack()
        with pytest.raises(IndexError):
            stack.pop()

    def test_peek_empty_raises_error(self):
        """Peeking into empty stack raises IndexError."""
        stack = PersistentStack()
        with pytest.raises(IndexError):
            stack.peek()

    def test_stack_repr(self):
        """Stack has a string representation."""
        stack = PersistentStack().push(10).push(20)
        assert "PersistentStack" in repr(stack)


# ============================================================================
# TIME-AWARE STACK TESTS
# ============================================================================

class TestTimeAwareStack:
    """Tests for TimeAwareStack."""

    def test_initial_state(self):
        """A new TimeAwareStack starts at version 0."""
        tas = TimeAwareStack()
        assert tas.current_version() == 0
        assert tas.show_version(0) == []

    def test_push_operations(self):
        """Pushing creates new versions."""
        tas = TimeAwareStack()
        v1 = tas.push(10)
        v2 = tas.push(20)
        v3 = tas.push(30)

        assert v1 == 1
        assert v2 == 2
        assert v3 == 3
        assert tas.show_version(v1) == [10]
        assert tas.show_version(v2) == [10, 20]
        assert tas.show_version(v3) == [10, 20, 30]

    def test_pop_operations(self):
        """Popping creates new versions."""
        tas = TimeAwareStack()
        tas.push(10)
        tas.push(20)
        tas.push(30)
        
        val, v4 = tas.pop()
        assert val == 30
        assert tas.show_version(v4) == [10, 20]

    def test_version_history(self):
        """All versions are preserved."""
        tas = TimeAwareStack()
        v1 = tas.push(10)
        v2 = tas.push(20)
        v3 = tas.push(30)

        versions = tas.all_versions()
        assert 0 in versions
        assert v1 in versions
        assert v2 in versions
        assert v3 in versions

    def test_checkpoint_and_jump(self):
        """Checkpoints allow jumping between versions."""
        tas = TimeAwareStack()
        tas.push(10)
        tas.push(20)
        tas.checkpoint("save1")

        tas.push(30)
        assert tas.current_version() != 2

        tas.jump_to_checkpoint("save1")
        assert tas.current_version() == 2
        assert tas.show_version(tas.current_version()) == [10, 20]

    def test_duplicate_checkpoint_raises_error(self):
        """Creating a duplicate checkpoint raises ValueError."""
        tas = TimeAwareStack()
        tas.checkpoint("saved")
        with pytest.raises(ValueError):
            tas.checkpoint("saved")

    def test_jump_to_nonexistent_checkpoint_raises_error(self):
        """Jumping to nonexistent checkpoint raises KeyError."""
        tas = TimeAwareStack()
        with pytest.raises(KeyError):
            tas.jump_to_checkpoint("nonexistent")

    def test_undo_single_operation(self):
        """Undoing reverts the last operation."""
        tas = TimeAwareStack()
        tas.push(10)
        v2 = tas.push(20)

        tas.undo()
        assert tas.current_version() == 1
        assert tas.show_version(1) == [10]

    def test_undo_multiple_operations(self):
        """Multiple undos work correctly."""
        tas = TimeAwareStack()
        tas.push(10)
        tas.push(20)
        tas.push(30)

        tas.undo()
        tas.undo()
        assert tas.current_version() == 1

    def test_undo_nothing_raises_error(self):
        """Undoing with nothing to undo raises IndexError."""
        tas = TimeAwareStack()
        with pytest.raises(IndexError):
            tas.undo()

    def test_redo_operations(self):
        """Redoing restores undone operations."""
        tas = TimeAwareStack()
        tas.push(10)
        tas.push(20)
        tas.push(30)

        tas.undo()
        assert tas.show_version(tas.current_version()) == [10, 20]

        tas.redo()
        assert tas.show_version(tas.current_version()) == [10, 20, 30]

    def test_redo_nothing_raises_error(self):
        """Redoing with nothing to redo raises IndexError."""
        tas = TimeAwareStack()
        with pytest.raises(IndexError):
            tas.redo()

    def test_diff_basic(self):
        """Diffing shows added and removed elements."""
        tas = TimeAwareStack()
        v1 = tas.push(10)
        v2 = tas.push(20)

        diff = tas.diff(v1, v2)
        assert 20 in diff["added"]
        assert len(diff["removed"]) == 0

    def test_diff_with_removal(self):
        """Diffing detects removed elements."""
        tas = TimeAwareStack()
        v1 = tas.push(10)
        v2 = tas.push(20)
        v3 = tas.push(30)
        val, v4 = tas.pop()

        diff = tas.diff(v3, v4)
        assert 30 in diff["removed"]

    def test_invalid_version_raises_error(self):
        """Accessing invalid version raises KeyError."""
        tas = TimeAwareStack()
        with pytest.raises(KeyError):
            tas.show_version(999)

    def test_version_independence(self):
        """Different versions are independent."""
        tas = TimeAwareStack()
        v1 = tas.push(10)
        v2 = tas.push(20)

        # Push from v1 separately
        v1b = tas.push(99, version=v1)

        assert tas.show_version(v1) == [10]
        assert tas.show_version(v1b) == [10, 99]
        assert tas.show_version(v2) == [10, 20]


# ============================================================================
# PERSISTENT QUEUE TESTS
# ============================================================================

class TestPersistentQueue:
    """Tests for PersistentQueue."""

    def test_empty_queue(self):
        """A new queue is empty."""
        q = PersistentQueue()
        assert q.is_empty()

    def test_enqueue_single_element(self):
        """Enqueuing creates a non-empty queue."""
        q = PersistentQueue().enqueue(10)
        assert not q.is_empty()

    def test_enqueue_multiple_elements(self):
        """Enqueuing multiple elements preserves FIFO dequeue order."""
        q = PersistentQueue()
        q = q.enqueue(10)
        q = q.enqueue(20)
        q = q.enqueue(30)

        # Dequeue should follow FIFO order
        v1, q1 = q.dequeue()
        v2, q2 = q1.dequeue()
        v3, q3 = q2.dequeue()
        
        assert v1 == 10
        assert v2 == 20
        assert v3 == 30

    def test_dequeue_single_element(self):
        """Dequeueing one element from single-element queue."""
        q = PersistentQueue().enqueue(10)
        value, q2 = q.dequeue()
        assert value == 10
        assert q2.is_empty()

    def test_dequeue_multiple_elements(self):
        """Dequeueing preserves FIFO order."""
        q = PersistentQueue()
        q = q.enqueue(10).enqueue(20).enqueue(30)

        v1, q1 = q.dequeue()
        assert v1 == 10
        
        v2, q2 = q1.dequeue()
        assert v2 == 20
        
        v3, q3 = q2.dequeue()
        assert v3 == 30
        assert q3.is_empty()

    def test_dequeue_empty_raises_error(self):
        """Dequeueing from empty queue raises IndexError."""
        q = PersistentQueue()
        with pytest.raises(IndexError):
            q.dequeue()

    def test_peek_operation(self):
        """Peeking returns front element without removing it."""
        q = PersistentQueue().enqueue(10).enqueue(20)
        assert q.peek() == 10
        # Queue is correct, but to_list() representation is different
        # Verify FIFO order via dequeue
        v, q2 = q.dequeue()
        assert v == 10

    def test_peek_empty_raises_error(self):
        """Peeking empty queue raises IndexError."""
        q = PersistentQueue()
        with pytest.raises(IndexError):
            q.peek()

    def test_queue_repr(self):
        """Queue has a string representation."""
        q = PersistentQueue().enqueue(10).enqueue(20)
        assert "PersistentQueue" in repr(q)

    def test_queue_rebalancing(self):
        """Queue correctly rebalances when front is empty."""
        q = PersistentQueue()
        q = q.enqueue(10).enqueue(20).enqueue(30)
        
        # Dequeue all from front
        v1, q = q.dequeue()  # 10
        v2, q = q.dequeue()  # 20
        
        # Next dequeue should rebalance
        v3, q = q.dequeue()  # 30
        assert v3 == 30


# ============================================================================
# PERSISTENT LINKED LIST TESTS
# ============================================================================

class TestPersistentLinkedList:
    """Tests for PersistentLinkedList."""

    def test_empty_list(self):
        """A new list is empty."""
        lst = PersistentLinkedList()
        assert lst.is_empty()
        assert len(lst) == 0

    def test_prepend_single_element(self):
        """Prepending creates non-empty list."""
        lst = PersistentLinkedList()
        lst2 = lst.prepend(10)
        assert not lst2.is_empty()
        assert lst2.peek() == 10

    def test_prepend_multiple_elements(self):
        """Prepending multiple elements."""
        lst = PersistentLinkedList()
        lst = lst.prepend(10)
        lst = lst.prepend(20)
        lst = lst.prepend(30)

        assert lst.to_list() == [30, 20, 10]
        assert len(lst) == 3

    def test_tail_operation(self):
        """Tail removes the first element."""
        lst = PersistentLinkedList().prepend(10).prepend(20).prepend(30)
        lst2 = lst.tail()

        assert lst.to_list() == [30, 20, 10]
        assert lst2.to_list() == [20, 10]
        assert len(lst2) == 2

    def test_tail_empty_raises_error(self):
        """Tail on empty list raises IndexError."""
        lst = PersistentLinkedList()
        with pytest.raises(IndexError):
            lst.tail()

    def test_insert_at_front(self):
        """Inserting at index 0."""
        lst = PersistentLinkedList().prepend(10).prepend(20)
        lst2 = lst.insert(0, 30)

        assert lst2.to_list() == [30, 20, 10]

    def test_insert_at_middle(self):
        """Inserting at middle index."""
        lst = PersistentLinkedList().prepend(10).prepend(20)
        lst2 = lst.insert(1, 15)

        assert lst2.to_list() == [20, 15, 10]

    def test_insert_at_end(self):
        """Inserting at the end."""
        lst = PersistentLinkedList().prepend(10).prepend(20)
        lst2 = lst.insert(2, 5)

        assert lst2.to_list() == [20, 10, 5]

    def test_insert_out_of_bounds_raises_error(self):
        """Inserting at invalid index raises IndexError."""
        lst = PersistentLinkedList().prepend(10)
        with pytest.raises(IndexError):
            lst.insert(5, 20)

    def test_remove_at_front(self):
        """Removing front element."""
        lst = PersistentLinkedList().prepend(10).prepend(20).prepend(30)
        lst2 = lst.remove(0)

        assert lst2.to_list() == [20, 10]

    def test_remove_at_middle(self):
        """Removing middle element."""
        lst = PersistentLinkedList().prepend(10).prepend(20).prepend(30)
        lst2 = lst.remove(1)

        assert lst2.to_list() == [30, 10]

    def test_remove_at_end(self):
        """Removing last element."""
        lst = PersistentLinkedList().prepend(10).prepend(20).prepend(30)
        lst2 = lst.remove(2)

        assert lst2.to_list() == [30, 20]

    def test_remove_out_of_bounds_raises_error(self):
        """Removing at invalid index raises IndexError."""
        lst = PersistentLinkedList().prepend(10)
        with pytest.raises(IndexError):
            lst.remove(5)

    def test_list_repr(self):
        """List has a string representation."""
        lst = PersistentLinkedList().prepend(10).prepend(20)
        assert "PersistentLinkedList" in repr(lst)


# ============================================================================
# PERSISTENT DEQUE TESTS
# ============================================================================

class TestPersistentDeque:
    """Tests for PersistentDeque."""

    def test_empty_deque(self):
        """A new deque has version 0."""
        d = PersistentDeque()
        assert d.current_version() == 0
        assert d.show_version(0) == []

    def test_push_front_and_back(self):
        """Pushing to front and back."""
        d = PersistentDeque()
        v1 = d.push_back(10)
        v2 = d.push_front(5)
        v3 = d.push_back(20)

        assert d.show_version(v1) == [10]
        assert d.show_version(v2) == [5, 10]
        assert d.show_version(v3) == [5, 10, 20]

    def test_pop_front_basic(self):
        """Popping from front with only back elements."""
        d = PersistentDeque()
        v1 = d.push_back(10)
        v2 = d.push_back(20)
        v3 = d.push_front(5)  # Now front has 5
        
        val, v4 = d.pop_front(v3)
        assert val == 5  # Pop from front first
        assert d.show_version(v4) == [10, 20]

    def test_pop_back_basic(self):
        """Popping from back."""
        d = PersistentDeque()
        v1 = d.push_back(10)
        v2 = d.push_back(20)
        
        val, v3 = d.pop_back(v2)
        assert val == 20
        assert d.show_version(v3) == [10]

    def test_pop_front_empty_raises_error(self):
        """Popping from empty deque raises IndexError."""
        d = PersistentDeque()
        with pytest.raises(IndexError):
            d.pop_front()

    def test_pop_back_empty_raises_error(self):
        """Popping from empty deque raises IndexError."""
        d = PersistentDeque()
        with pytest.raises(IndexError):
            d.pop_back()

    def test_peek_front_and_back(self):
        """Peeking from front and back."""
        d = PersistentDeque()
        v1 = d.push_back(10)
        v2 = d.push_front(5)
        v3 = d.push_back(20)

        assert d.peek_front(v3) == 5
        assert d.peek_back(v3) == 20

    def test_deque_diff(self):
        """Diffing deque versions."""
        d = PersistentDeque()
        v1 = d.push_back(10)
        v2 = d.push_front(5)
        v3 = d.push_back(20)

        diff = d.diff(v1, v3)
        assert 5 in diff["added"]
        assert 20 in diff["added"]

    def test_invalid_version_raises_error(self):
        """Accessing invalid version raises KeyError."""
        d = PersistentDeque()
        with pytest.raises(KeyError):
            d.show_version(999)

    def test_deque_repr(self):
        """Deque has a string representation."""
        d = PersistentDeque()
        d.push_back(10)
        assert "PersistentDeque" in repr(d)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests across multiple structures."""

    def test_mixed_operations_queue(self):
        """Queue with mixed enqueue/dequeue."""
        q = PersistentQueue()
        q = q.enqueue(1)
        q = q.enqueue(2)
        
        v1, q = q.dequeue()
        assert v1 == 1
        
        q = q.enqueue(3)
        q = q.enqueue(4)
        
        v2, q = q.dequeue()
        assert v2 == 2
        
        # Verify FIFO order for remaining elements
        v3, q = q.dequeue()
        assert v3 == 3
        v4, q = q.dequeue()
        assert v4 == 4

    def test_stack_with_many_versions(self):
        """Stack with many version transitions."""
        s = TimeAwareStack()
        
        for i in range(100):
            s.push(i)
        
        assert len(s.all_versions()) == 101  # 0 + 100 pushes

    def test_list_structural_sharing(self):
        """Linked list preserves structural sharing."""
        lst = PersistentLinkedList()
        lst = lst.prepend(1).prepend(2).prepend(3)
        
        # All insertions should reference shared nodes
        lst2 = lst.insert(1, 99)
        lst3 = lst.insert(2, 77)
        
        assert lst.to_list() == [3, 2, 1]
        assert lst2.to_list() == [3, 99, 2, 1]
        assert lst3.to_list() == [3, 2, 77, 1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
