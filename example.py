#Working Proof

from timelock.stack import TimeAwareStack

s = TimeAwareStack()

v1 = s.push(10)
v2 = s.push(20)
v3 = s.push(30)

print(s.peek(v1))
print(s.peek(v2))
print(s.peek(v3))

value, v4 = s.pop(v3)
print(value)
print(s.peek(v2))