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
        is_left_satisfied = True
        is_right_satisfied = True

        if node.left:
            if node.value > node.left.value:
                return False
            else:
                is_left_satisfied = Heap._is_heap_satisfied(node.left)
        
        if node.right:
            if node.value > node.right.value:
                return False
            else:
                is_right_satisfied = Heap._is_heap_satisfied(node.right)

        return is_right_satisfied and is_left_satisfied

    def insert(self, value):
        '''
        Inserts value into the heap.
        '''
        if self.root is None:
            self.root = Node(value)
            self.root.descendents = 1
        else:
            self.root = Heap._insert(self.root,value)

    @staticmethod
    def _insert(node, value):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None: 
            return 
       
       #if no space, go left (complete tree)
        if node.left and node.right:
            node.left = Heap._insert(node.left,value)
            if node.value > node.left.value: 
                return Heap._move_up(node,value)
        
        if node.left is None: 
            node.left = Node(value)
            #if heap not satisfied, trickle up 
            if node.value > node.left.value:  
                return Heap._move_up(node, value)
        
        elif node.right is None: 
            node.right = Node(value) 
            #if heap not satisfied, tricke up
            if node.value > node.right.value:
                return Heap._move_up(node, value)
        
        return node

    @staticmethod
    def _move_up(node, value):
        '''
        finds the recently inserted value and swaps up until it finds a sweet spot
        '''
        
        if Heap._is_heap_satisfied(node) == True: 
            return node
        #go down to leaves
        if node.left and node.left.value > node.value:
            node.left = Heap._move_up(node.left, value)
        if node.right and node.right.value > node.value:
            node.right = Heap._move_up(node.right, value)
        if node.left: 
            #if value, trickle up
            if node.left.value == value: 
                new_parent = node.left.value
                new_left = node.value
                
                node.value = new_parent
                node.left.value = new_left
        
        if node.right:
            #if value, trickle up
            if node.right.value == value: 
                new_parent = node.right.value
                new_right = node.value

                node.value = new_parent
                node.right.value = new_right

        return node

    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)
            
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
        #if heap is empty
        if self.root is None: 
            return None
        #if heap is root
        elif self.root.left is None and self.root.right is None:
            self.root = None
        else:
            #store value to replace root
            replace_right = Heap._find_right(self.root)
            #remove such value from tree
            self.root = Heap._remove(self.root)
            if replace_right == self.root.value:
                return 
            else:
                #replace root's value with value furthest right
                self.root.value = replace_right
            #if not satisfied, trickle down
            if Heap._is_heap_satisfied(self.root) == False: 
                return Heap._move_down(self.root)

    @staticmethod
    def _remove(node):
        '''
        removes the node that is now the root
        '''
        if node is None: 
            return 
        elif node.right:
            node.right = Heap._remove(node.right)
        elif node.left:
            node.left = Heap._remove(node.left)
        else: 
            #remove node that is furthest to the right
            if node.right is None and node.left is None: 
                return None
    
        return node

    @staticmethod
    def _find_right(node):
        '''
        finds value furthest to the right to replace the root
    
        '''
        if node.left is None and node.right is None:
            #returns value furthest to the right
            return node.value
        elif node.right:
            return Heap._find_right(node.right)
        elif node.left:
            return Heap._find_right(node.left)
        
    @staticmethod
    def _move_down(node):
        '''
        trickle the new root down until it finds a sweet spot
        '''
        if node.left is None and node.right is None: 
            return node
            
        if node.left and (node.right is None or node.left.value <= node.right.value): 
            if node.left.value < node.value: 
                new_parent = node.left.value
                new_left = node.value
                
                node.value = new_parent
                node.left.value = new_left
            
            node.left = Heap._move_down(node.left)
        
        elif node.right and (node.left is None or node.right.value <= node.left.value): 
            if node.right.value < node.value: 
                new_parent = node.right.value
                new_right = node.value

                node.value = new_parent
                node.right.value = new_right
            
            node.right = Heap._move_down(node.right)
        
        return node
