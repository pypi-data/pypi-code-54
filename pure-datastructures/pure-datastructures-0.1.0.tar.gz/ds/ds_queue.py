class Queue:

    def __init__(self):
        """
        Initialize Queue. params:
        :items: Array and empty
        """
        self.items = []

    def is_empty(self):
        """Check queue is Empty or not"""
        return self.items == []

    def procedure_enqueue(self, item):
        """Push new object to queue"""
        self.items.insert(0, item)

    def procedure_dequeue(self):
        """Remove first object from queue."""
        return self.items.pop()

    def procedure_expand_size(self):
        """Count object from queue."""
        return len(self.items)