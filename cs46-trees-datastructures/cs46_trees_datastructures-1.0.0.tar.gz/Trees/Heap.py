'''
'''

from Trees.BinaryTree import BinaryTree, Node

class Heap(BinaryTree):
    '''
    FIXME:
    Heap is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above 
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the Heap.
        '''
        super().__init__()
        if xs is not None:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command Heap([1,2,3])
        it's __repr__ will return "Heap([1,2,3])"

        For the Heap, type(self).__name__ will be the string "Heap",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of Heap will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__+'('+str(self.to_list('inorder'))+')'


    def is_heap_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return Heap._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node): #ask about stack overflow
        '''
        FIXME:
        Implement this method.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
        right_satisfied = True
        left_satisfied = True
        if node is None:
            return True
        if node.left:
            if  node.value <= node.left.value and Heap._is_heap_satisfied(node.left):
                left_satisfied = True
            else:
                left_satisfied = False
        if node.right:
            if node.value <= node.right.value and Heap._is_heap_satisfied(node.right):
                right_satisfied = True
            else:
                right_satisfied = False
        if right_satisfied == True and left_satisfied == True:
            return True
        else:
            return False

    def insert(self, value):
        '''
        Inserts value into the heap.
        '''
        if self.root is None:
            self.root = Node(value)
            self.root.descendents = 1
        else:
            Heap._insert(value, self.root)


    @staticmethod
    def _insert(value, node): #how best to tell where the right place to insert is?
        '''
        FIXME:
        Implement this function.
        '''

        node.descendents +=1

        binary = "{0:b}".format(node.descendents) #takes descendents and prints it in a string of binary. the first digit is gauranteed to be a 1. converts it into a single string
        if binary[1] == '0': #need to take this code to adapt it to go to the right direction. right now goes to left
            if node.left is None: #means we have gotten to the bottom of the tree, there is no child we are at a leaf node so at this point we have to add our node
                node.left = Node(value)
                node.left.descendents = 1
            else:
                Heap._insert(value, node.left)
            if node.value > node.left.value:    #handles the swapping positions
                node.value, node.left.value = node.left.value, node.value

            #right side
        if binary[1] == '1':
            if node.right is None:
                node.right = Node(value)
                node.right.descendents = 1
            else:
                Heap._insert(value, node.right)
            if node.value > node.right.value:
                node.value, node.right.value = node.right.value, node.value

    


    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        for a in xs:
            self.insert(a)

    def find_smallest(self):  #for a min heap  #is this for a minheap or a maxheap? 
        '''
        Returns the smallest value in the tree.

        FIXME:
        Implement this function.
        This function is not implemented in the lecture notes,
        but if you understand the structure of a Heap it should be easy to implement.

        HINT:
        Create a recursive staticmethod helper function,
        similar to how the insert and find functions have recursive helpers.
        '''
        if self.root:
            return self.root.value

    def remove_min(self): #confused on theory for this method do I need more functions? 
        '''
        Removes the minimum value from the Heap. 
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.
        '''
        print("before remove min", self)
        if self.root is None or (self.root.left is None and self.root.right is None):
            self.root = None 
        else:
            last_element = Heap._remove_last_element(self.root)
            self.root.value = last_element
            Heap._swap(self.root)

    @staticmethod 
    def _remove_last_element(node):  
        binary = "{0:b}".format(node.descendents)
        node.descendents = node.descendents - 1
        if binary[1] == '0':
            if len(binary) == 2: 
                temp = node.left.value
                node.left = None
                return temp
            else:
                return Heap._remove_last_element(node.left)
        if binary[1] == '1':
            if len(binary) == 2:
                temp = node.right.value
                node.right = None
                return temp
            else:
                return Heap._remove_last_element(node.right)

    @staticmethod
    def _swap(node): 
        if node.left and node.right:
            if node.left.value <= node.right.value and node.left.value < node.value:
                node.value, node.left.value = node.left.value, node.value
                Heap._swap(node.left)
            elif node.right.value <=  node.left.value and node.right.value < node.value:
                node.value, node.right.value = node.right.value, node.value
                Heap._swap(node.right)
        elif node.left and (node.right is None): 
            if node.value > node.left.value:
                node.value, node.left.value = node.left.value, node.value
                Heap._swap(node.left)
        elif node.right and (node.left is None):
            if node.value > node.right.value:
                node.value, node.right.value = node.right.value, node.value
                Heap._swap(node.right)



