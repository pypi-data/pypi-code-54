class Queue:

    def __init__(self):
        self.items = []

    # check whether queue is empty or not
    def isEmpty(self):
        return self.items == []

    # push new object to queue
    def enqueue(self, item):
        self.items.insert(0, item)

    # remove first object from queue
    def dequeue(self):
        return self.items.pop()

    # count object from queue
    def size(self):
        return len(self.items)

"""
Only mock test

q = Queue()
q.enqueue(3)
q.enqueue('json')
q.dequeue()
q.enqueue(2)
q.isEmpty()

print(q.size())
"""