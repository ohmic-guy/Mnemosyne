from mnemosyne.stack import TimeAwareStack

s = TimeAwareStack()

v1 = s.push(10)
v2 = s.push(20)
v3 = s.push(30)

s.checkpoint("before_pop")

val, v4 = s.pop(v3)

print("All Versions:", s.all_versions())


for v in s.all_versions():
    print(f"Version {v}:", s.show_version(v))


s.jump_to_checkpoint("before_pop")
print("Current Version after checkpoint jump:", s.current_version())

s.undo()
print("After Undo:", s.show_version(s.current_version()))
s.redo()
print("After Redo:", s.show_version(s.current_version()))

s.visualize()