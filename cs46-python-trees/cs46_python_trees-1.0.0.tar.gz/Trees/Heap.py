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
            for x in xs:
                self.insert(x)

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
        left_sat = True
        right_sat = True
        if node is None:
            return True
        if node.left:
            left_sat = node.value <= node.left.value and Heap._is_heap_satisfied(node.left)
        if node.right:
            right_sat = node.value <= node.right.value and Heap._is_heap_satisfied(node.right)
        if left_sat and right_sat:
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
            Heap._insert(value, self.root, self.size())

    @staticmethod
    def _insert(value, node, size):
        '''
        FIXME:
        Implement this function.
        '''
        if node is None:
            node.value = value
        else:
            leaf = node
            binsize = str(bin(size + 1))
            for digit in binsize[3:-1]:
                if digit == '0':
                    leaf = leaf.left
                if digit == '1':
                    leaf = leaf.right
            if binsize[-1] == '0':
                leaf.left = Node(value)
            else:
                leaf.right = Node(value)
            if not Heap._is_heap_satisfied(node):
                binsize = binsize[2:]
                Heap._bubble_up(binsize, node)

    @staticmethod
    def _bubble_up(binsize, node):
        startnode = node
        if len(binsize) == 2:
            if binsize[-1] == '0':
                if node.value > node.left.value:
                    Heap.swap(node, node.left)
            else:
                if node.value > node.right.value:
                    Heap.swap(node, node.right)
        else:
            stack = []
            for digit in binsize[1:-1]:
                if digit == '0':
                    stack.append(node.left)
                    node = node.left
                if digit == '1':
                    stack.append(node.right)
                    node = node.right
            while len(stack) > 0:
                node = stack.pop()
                stack.append(node)
                if node.value > node.left.value:
                    stack.pop()
                    Heap.swap(node, node.left)
                    stack.append(node)
                elif node.right and node.value > node.right.value:
                    stack.pop()
                    Heap.swap(node, node.right)
                    stack.append(node)
                else:
                    stack.pop()
        if startnode.left and startnode.value > startnode.left.value:
            Heap.swap(startnode, startnode.left)
        elif startnode.right and startnode.value > startnode.right.value:
            Heap.swap(startnode, startnode.right)

    @staticmethod
    def swap(node1, node2):
        temp = node2.value
        node2.value = node1.value
        node1.value = temp
            
    def size(self):
        if self.root is None:
            return 0
        stack = []
        stack.append(self.root)
        size = 1
        while stack:
            node = stack.pop()
            if node.left:
                size += 1
                stack.append(node.left)
            if node.right:
                size += 1
                stack.append(node.right)
        return size

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
        return Heap._find_smallest(self.root)

    @staticmethod
    def _find_smallest(node):
        if node is None:
            return
        else:
            return node.value

    @staticmethod
    def _bubble_down(node):
        leaf = node
        if leaf:
            if leaf.left and leaf.right is None:
                if leaf.left.value < leaf.value:
                    Heap.swap(leaf, leaf.left)
                leaf = leaf.left
            elif leaf.left and leaf.right:
                mini = min(leaf.left.value, leaf.right.value)
                if mini == leaf.left.value:
                    if mini < leaf.value:
                        Heap.swap(leaf, leaf.left)
                    leaf = leaf.left
                else:
                    if mini < leaf.value:
                        Heap.swap(leaf, leaf.right)
                    leaf = leaf.right
            else:
                return
            return Heap._bubble_down(leaf)

    def remove_min(self):
        '''
        Removes the minimum value from the Heap. 
        If the heap is empty, it does nothing.

        FIXME:
        Implement this function.
        '''
        if self.root is None:
            return
        elif self.size() == 1:
            self.root = None
        else:
            Heap._remove_min(self.root, self.size())
            Heap._bubble_down(self.root)

    @staticmethod
    def _remove_min(node, size):
        leaf = node
        binsize = str(bin(size))
        binsize = binsize[2:]
        if len(binsize) == 2:
            if binsize[-1] == '0':
                replacement = leaf.left
                Heap.swap(node, replacement)
                leaf.left = None
            else:
                replacement = leaf.right
                Heap.swap(node, replacement)
                leaf.right = None
        else:
            for digit in binsize[1:-1]:
                if digit == '0':
                    leaf = leaf.left
                if digit == '1':
                    leaf = leaf.right
            if binsize[-1] == '0':
                replacement = leaf.left
                Heap.swap(node, replacement)
                leaf.left = None
            else:
                replacement = leaf.right
                Heap.swap(node, replacement)
                leaf.right = None
