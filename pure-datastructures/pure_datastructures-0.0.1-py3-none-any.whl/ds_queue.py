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

q = Queue()
q.enqueue(3)
q.enqueue('json')
q.dequeue()
q.enqueue(2)
q.isEmpty()
print(q.size())

def hotPotato(name, num):
    queue = Queue()
    for n in name:
        queue.enqueue(n)

    while queue.size() > 1:
        for i in range(num):
            queue.enqueue(queue.dequeue())

        queue.dequeue()

    return queue.dequeue()

print(hotPotato(['Ryan', 'Adi', 'Bima', 'Madi'],2))

class Printer:

    def __init__(self, page):
        self.pagerate = page
        self.current_task = None
        self.time_remains = 0

    def countdown(self):
        if self.current_task != None:
            self.time_remains = time_remains - 1
            if self.time_remains <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def next(self):
        self.current_task = new_task
        self.time_remains = new_task.getPage() * 60/self.pagerate

import random

class Task:

    def __init__(self, time):
        self.timestamp = time
        self.pages = random.randrange(1,20)

    # get timestamp
    def getStamp(self):
        return self.timestamp

    # get pages for printing
    def getPage(self):
        return self.pages

    def wait(self, current_time):
        return current_time - self.timestamp

def simulation(numSecs, pagesPerMins):

    printer = Printer(pagesPerMins)
    printQueue = Queue()
    waitingList = []

    for currentSecs in range(numSecs):
        if newPrint():
            task = Task(currentSecs)
            printQueue.enqueue(task)

        if (not printer.busy()) and (not printQueue.isEmpty()):
            next_task = printQueue.dequeue()
            waitingList.append(next_task.wait(currentSecs))
	    printer.next(next_task)

        printer.countdown()

    averageWait = sum(waitingList) / len(waitingList)
    print("Average wait is %6.2f secs %3d task remains." %(averageWait, printQueue.size()))

def newPrint():
    
    num = random.randrange(1, 181)
    if num == 180:
        return True
    else:
        return False

for i in range(10):
    simulation(3600, 5)
