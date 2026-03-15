# example_deque_diff.py

from mnemosyne.deque import PersistentDeque

d = PersistentDeque()

# Version 1: push back
v1 = d.push_back(10)

# Version 2: push front
v2 = d.push_front(5)

# Version 3: push back again
v3 = d.push_back(20)

# Version 4: pop front
val, v4 = d.pop_front(v3)

print("Popped value at v4:", val)
print()

# Show states
print("Deque at v1:", d.show_version(v1))
print("Deque at v2:", d.show_version(v2))
print("Deque at v3:", d.show_version(v3))
print("Deque at v4:", d.show_version(v4))
print()

# Diff examples
print("Diff v1 → v3:")
print(d.diff(v1, v3))
print()

print("Diff v3 → v4:")
print(d.diff(v3, v4))
