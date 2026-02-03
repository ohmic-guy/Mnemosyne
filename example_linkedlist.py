from mnemosyne.linkedlist import PersistentLinkedList

v0 = PersistentLinkedList()
v1 = v0.prepend(10)
v2 = v1.prepend(20)
v3 = v2.insert(1, 15)
v4 = v3.remove(0)

print(v0.to_list())
print(v1.to_list())
print(v2.to_list())
print(v3.to_list())
print(v4.to_list())