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
        if xs:
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
            return self._is_heap_satisfied(self.root)
        return True

    @staticmethod
    def _is_heap_satisfied(node):
        '''
        FIXME:
        Implement this method.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
    
        is_left_satisfied = True
        is_right_satisfied= True

        if node.left:
            if node.value <= node.left.value:
                is_left_satisfied = Heap._is_heap_satisfied(node.left)
            else:
                is_left_satisfied = False
        if node.right:
            if node.value <= node.right.value:
                is_right_satisfied = Heap._is_heap_satisfied(node.right)
            else:
                is_right_satisfied = False
        return is_left_satisfied and is_right_satisfied

    def insert(self, value):
        '''
        Inserts value into the heap.
        '''
        if self.root is None:
            self.root = Node(value)
            self.root.descendents = 1
        else:
            Heap._insert(self.root, value)


    @staticmethod
    def _insert(node, value):
        node.descendents += 1
        binary = "{0:b}".format(node.descendents)
        if binary[1] == '0':        # go to left
            if node.left is None:
                node.left = Node(value)
                node.left.descendents = 1
            else:
                Heap._insert(node.left, value)
            if node.value > node.left.value:
                node.value, node.left.value = node.left.value, node.value
        if binary[1] == '1':      # go to right
            if node.right is None:
                node.right = Node(value)
                node.right.descendents = 1
            else:
                Heap._insert(node.right, value)
            if node.value > node.right.value:
                node.value, node.right.value = node.right.value, node.value
        
         
    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.

        FIXME:
        Implement this function.
        '''
        if xs:
            return [self.insert(x) for x in xs]

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
            return self.root.value
    
    @staticmethod
    def _delete_last(node):
        binary = "{0:b}".format(node.descendents)
        if node.left is None and node.right is None:  # node has no children
            return node.value
        node.descendents -= 1
        if binary[1] == '0':        # the leaf node is on the left
            if len(binary) == 2:        # base case at parent of left leaf node
                store_left = node.left.value
                node.left = None
                return store_left       # return the deleted last node to swap
            else:
                return Heap._delete_last(node.left)
        elif binary[1] == '1':      # the leaf node is on the right
            if len(binary) == 2:        # base case at parent of right leaf node
                store_right = node.right.value
                node.right = None
                return store_right      # return the deleted last node to swap
            else:
                return Heap._delete_last(node.right)               


  


    def remove_min(self):
        '''
        Removes the minimum value from the Heap. 
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.
        '''
        if self.root is None or (self.root.left is None and self.root.right is None):
            self.root = None
        else:
            deleted_leaf_node = Heap._delete_last(self.root)
            self.root.value = deleted_leaf_node    # sets root's value = value of the deleted last node
            Heap._swap(self.root)                    # swaps the nodes until heap is satisfied       

 
  
   
    @staticmethod
    def _swap(node):
        if node.left and node.right:
            if node.left.value <= node.right.value and node.left.value < node.value:
                node.value, node.left.value = node.left.value, node.value
                Heap._swap(node.left)
            elif node.right.value <= node.left.value and node.right.value < node.value:
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

