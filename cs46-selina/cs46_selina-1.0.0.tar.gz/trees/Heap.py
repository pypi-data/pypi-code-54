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
        left = True
        right = True
        if node.left:
            if node.value <= node.left.value:
                left = Heap._is_heap_satisfied(node.left)
            else:
                return False
        if node.right:
            if node.value <= node.right.value:
                right = Heap._is_heap_satisfied(node.right)
            else:
                return False
        return right and left
     
    @staticmethod
    def size(node):

        if node is None:
            return 0
        stack=[]
        stack.append(node)
        size=1
        while stack:
            node=stack.pop()
            if node.left:
                size+=1
                stack.append(node.left)
            if node.right:
                size+=1
                stack.append(node.right)
        return size
  
    def insert(self, value):
        '''
        Inserts value into the heap.
        '''
        if self.root is None:
            self.root = Node(value)
            self.root.descendents = 1
            self.root.parent=None
        else:
            tree_size = Heap.size(self.root)
            tree_size = tree_size + 1
            tree_size = bin(tree_size).replace("0b", "")
            tree_size = tree_size[1:]
            cur_node = self.root
            for num in tree_size[:-1]:
                if num == '0':
                    cur_node = cur_node.left
                if num == '1':
                    cur_node = cur_node.right
            if tree_size[-1] == '0':
                cur_node.left = Node(value)
                cur_node.left.parent=cur_node
                self.root = Heap._trickle_up(cur_node.left)
            else:
                cur_node.right = Node(value)
                cur_node.right.parent=cur_node
                self.root = Heap._trickle_up(cur_node.right)

    @staticmethod
    def _trickle_up(node):
        if node.parent==None:
            return node
        if node.value<node.parent.value:
            swap=node.parent.value
            node.parent.value=node.value
            node.value=swap
            return Heap._trickle_up(node)
        else:
            return Heap._trickle_up(node.parent)
            


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
        node = self.root
        return Heap._find_smallest(node).value
        
    
    @staticmethod
    def _find_smallest(node):
        return node


    def remove_min(self):
        '''
        Removes the minimum value from the Heap. 
        If the heap is empty, it does nothing.
        FIXME:
        Implement this function.
        '''
        if self.root == None:
            pass
        if not self.root.left and not self.root.right:
            self.root = None
        else:
            self.root.value = None
            tree_size = Heap.size(self.root)
            tree_size = bin(tree_size).replace("0b", "")
            tree_size = tree_size[1:]
            cur_node = self.root
            for num in tree_size[:-1]:
                if num == '0':
                    cur_node = cur_node.left
                if num == '1':
                    cur_node = cur_node.right
            if tree_size[-1] == '0':
                swap_val = cur_node.left.value
                self.root.value = swap_val
                cur_node.left = None
            else:
                swap_val = cur_node.right.value
                self.root.value = swap_val
                cur_node.right = None
            Heap._trickle_down(self.root)
                
    @staticmethod
    def _trickle_down(node):
        if not node.left and not node.right:
            pass
        elif node.left and not node.right:
            if node.value>node.left.value:
                swap=node.value
                node.value=node.left.value
                node.left.value=swap
                Heap._trickle_down(node.left)
        elif node.right and not node.left:
            if node.value>node.right.value:
                swap=node.value
                node.value=node.right.value
                node.right.value=swap
                Heap._trickle_down(node.right)
        else:
            if node.value<node.right.value and node.value<node.left.value:
                pass
            elif node.left.value<node.right.value:
                swap=node.value
                node.value=node.left.value
                node.left.value=swap
                Heap._trickle_down(node.left)
            else:
                swap=node.value
                node.value=node.right.value
                node.right.value=swap
                Heap._trickle_down(node.right) 

            
        
        
