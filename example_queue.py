# example_queue.py

from mnemosyne.queue import PersistentQueue

q0 = PersistentQueue()
q1 = q0.enqueue(10)
q2 = q1.enqueue(20)
q3 = q2.enqueue(30)

v, q4 = q3.dequeue()
print(v)        # 10

v, q5 = q4.dequeue()
print(v)        # 20

print(q1.peek())  # 10 (old version still intact)