class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self, new_data):
        self.data = new_data

    def setNext(self, new_next):
        self.next = new_next

class OrderedList:

    def __init__(self):
        self.head = None

    def search_obj(self, item):
        current = self.head
        found = False
        stop = False

        while current != None and not found and not stop:
            if current.getData() == item:
                found = True
            else:
                if current.getData() > item:
                    stop = True
                else:
                    current = current.getNext()

        return found

    def add(self, item):
        current = self.head
        previous = None
        stop = False

        while current != None and not stop:
            if current.getData() > item:
                stop = True
            else:
                previous = current
                current = current.getNext()

        temporary = Node(item)
        if previous == None:
            temporary.setNext(self.head)
            self.head = temporary
        else:
            temporary.setNext(current)
            previous.setNext(temporary)

    def isEmpty(self):
        return self.head == None

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

# Mock test

search = OrderedList()

search.add(70)
search.add(31)
search.add(49)
search.add(50)
search.add(-10)
search.add(81)
search.add(26)

print(search.size())
print(search.search_obj(93))
print(search.search_obj(26))
