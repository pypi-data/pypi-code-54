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
        if xs :
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
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
    #Heap only have max and min max--parent > children, min--parent < children, but still need to be in order
    #trickle up/down
        left=True
        right=True 
        if node.left: 
            if node.value<=node.left.value:
                left= Heap._is_heap_satisfied (node.left)  
            else:
                return False
        if node.right:
            if node.value <=node.right.value:
                right= Heap._is_heap_satisfied (node.right)
            else:
                return False
        if node is None:
            return True 
        return left and right



    def insert(self, value):
        '''
        Inserts value into the heap.
        '''
        if self.root is None:
            self.root = Node(value)
            self.root.descendents = 1
        else:
            Heap._insert(value, self.root)

#insert from the next empty branch (by order)
# then swap spot, down/up
#use binary representation, get rid of the first digit
# 0 goes to the left, 1 goes to the right 
#need swap helper, down/up helper 



    @staticmethod
    def _insert(value, node):
        '''
        FIXME:
        Implement this function.
        '''
# 0 left 1 right

        node.descendents=node.descendents+1

        binary ="{0:b}".format(node.descendents)

        if binary[1] == '0':
            if node.left is None:
                node.left = Node(value)
                node.left.descendents =1 #indicate where to go 
            else:
                Heap._insert(value,node.left)
        #but if insert does not satisfy heap, then needs to swap
        # a min tree
            if node.left.value< node.value: # should be child > parent, trickle up 
        # swap! 
                node.left.value, node.value= node.value, node.left.value 


        if binary[1] =='1': #binary code, right
            if node.right is None:
                node.right = Node(value)
                node.right.descendents =1 #indicate where to go 
            else:
                Heap._insert(value,node.right)
        #but if insert does not satisfy heap, then needs to swap
        # a min tree
            if node.right.value< node.value: # should be child > parent, trickle up 
        # swap! 
                node.right.value, node.value= node.value, node.right.value 
    

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        FIXME:
        Implement this function.
        '''
        for i in xs:
            self.insert(i)

    def find_smallest(self):
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
            return Heap._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        return node.value

    def remove_min(self):
        '''
        Removes the minimum value from the Heap. 
        If the heap is empty, it does nothing.
        FIXME:
        Implement this function.
        '''
        #if the tree is empty, then nothing, remove is also none 
        #when you remove, you remove from the root, and then swap from nodes down
       #keep having new errors here, so define new here
       # if self.root is None:
          # pass
        #elif self.root.left and self.root.right is None:
           #self.root = None
        #elif self.root.left and self.root.right:
        #elif self.root.left is not None:
           #new= Heap._remove_last_node(self.root)
           #self.root.value = new
           #if not Heap._is_heap_satisfied(self.root):
               #Heap._swap(self.root)
        if self.root is None:
            pass
        elif self.root and self.root.left is None:
            self.root = None
        elif self.root.left and self.root.left:
            self.root.value = Heap._remove_last_node(self.root)
            if not Heap._is_heap_satisfied(self.root):
                Heap._swap(self.root)



    #helper function
    #remove_last_node, use the binary code
    # swap, use the same logic before, exchange value and also binary code     
    @staticmethod

    def _remove_last_node(node):
        #binary = "{0:b}".format(node.descendents)
        #node.descendents = node.descendents -1 
        #if len(binary) ==2:
           # if binary[1] =='1':
                #new=node.right
                #node.right = None
                #return new.value
            #else:
                #return Heap._remove_last_node(node.right)
        #else:
            #if binary[1] == '0':
                #new= node.left
                #node.left = None 
                #return new.value
            #else:
                #return Heap._remove_last_node(node.left)


        binary = "{0:b}".format(node.descendents) 
        node.descendents = node.descendents -1 
        if len(binary) == 2:
            if binary[1] == '1':
                new = node.right
                node.right = None
            elif binary[1] == '0':
                new = node.left
                node.left = None
            return new.value
        else:
            if binary[1] == '0':
                return Heap._remove_last_node(node.left) 
            elif binary[1] == '1':
                return Heap._remove_last_node(node.right)

    def _swap(node):
        #situation 1 tree is empty
        if node.left is None and node.right is None:
            return node 
        #situation 2, both of left and right exists and compare
        elif node.left and node.right:
            if node.left.value <= node.right.value and node.left.value<node.value:
                node.value, node.left.value = node.left.value, node.value
                Heap._swap(node.left)
            elif node.left.value >= node.right.value and node.right.value<node.value:
                node.value, node.right.value = node.right.value, node.value
                Heap._swap(node.right)
        # situation 3, only left exists
        elif node.left and node.right is None:
            if node.left.value < node.value:
                node.value, node.left.value = node.left.value, node.value
                Heap._swap(node.left)
       #situation4, only right exists
        elif node.right and node.left is None:
            if node.right.value < node.value:
                node.value, node.right.value = node.right.value, node.value
                Heap._swap(node.right)



