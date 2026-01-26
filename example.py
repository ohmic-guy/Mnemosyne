from mnemosyne.stack import TimeAwareStack

s = TimeAwareStack()

v1 = s.push(10)
v2 = s.push(20)
v3 = s.push(30)

# Named checkpoint
s.checkpoint("before_pop")

val, v4 = s.pop(v3)

# Show all versions
print("All Versions:", s.all_versions())

# Show stack snapshots
for v in s.all_versions():
    print(f"Version {v}:", s.show_version(v))

# Jump to checkpoint
s.jump_to_checkpoint("before_pop")
print("Current Version after checkpoint jump:", s.current_version())

# Undo / Redo
s.undo()
print("After Undo:", s.show_version(s.current_version()))
s.redo()
print("After Redo:", s.show_version(s.current_version()))

# Visualize
s.visualize()