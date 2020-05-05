from Trees.BinaryTree import BinaryTree, Node

class Heap(BinaryTree):

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

        is_left_satisfied = True
        is_right_satisfied = True

        if node is None:
            return True

        if node.left:
            is_left_satisfied = node.left.value >= node.value and Heap._is_heap_satisfied(node.left)

        if node.right:
            is_right_satisfied = node.right.value >= node.value and Heap._is_heap_satisfied(node.right)

        return is_right_satisfied and is_left_satisfied


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
    def _insert(value, node):
        '''
        use binary representation of total nodes to determine which subtree to go
        '''
        node.descendents += 1
        binary = "{0:b}".format(node.descendents)
        if binary[1] == '0':
            if node.left is None:
                node.left = Node(value)
                node.left.descendents = 1
            else:
                Heap._insert(value,node.left)
            if node.value > node.left.value:
                node.value, node.left.value = node.left.value, node.value
        elif binary[1] == '1':
            if node.right is None:
                node.right = Node(value)
                node.right.descendents = 1
            else:
                Heap._insert(value,node.right)
            if node.value > node.right.value:
                node.value, node.right.value = node.right.value, node.value


    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        '''
        for x in xs:
            self.insert(x)


    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
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
        '''
        if self.root is None:
            pass
        elif self.root and self.root.left is None:
            self.root = None
        elif self.root and self.root.left:
            self.root.value = Heap._remove_last_element(self.root)
            if not Heap._is_heap_satisfied(self.root):
                Heap._swap(self.root)


    @staticmethod
    def _remove_last_element(node):
        binary = "{0:b}".format(node.descendents)
        node.descendents -= 1
        if len(binary) == 1:
            node = None
        if len(binary) == 2:
            if binary[1] == '1':
                tmp = node.right
                node.right = None
            elif binary[1] == '0':
                tmp = node.left
                node.left = None
            return tmp.value
        else:
            if binary[1] == '0':
                return Heap._remove_last_element(node.left)
            elif binary[1] == '1':
                return Heap._remove_last_element(node.right)


    @staticmethod
    def _swap(node):
        if node.left is None and node.right is None:
            return node
        elif node.right is None:
            node.value, node.left.value = node.left.value, node.value
            return node
        else:
            if node.left.value < node.right.value:
                node.value, node.left.value = node.left.value, node.value
                if not Heap._is_heap_satisfied(node):
                    Heap._swap(node.left)
            else:
                node.value, node.right.value = node.right.value, node.value
                if not Heap._is_heap_satisfied(node):
                    Heap._swap(node.right)


'''
heap = Heap()
heap.insert(1)
heap.insert(2)
heap.insert(3)
heap.insert(4)
heap.insert(5)
heap.insert(6)
heap.insert(7)
heap.insert(8)
heap.insert(9)
heap.insert(10)
heap.insert(11)
print(heap.print_tree('inorder'))
heap.remove_min()
print(heap.print_tree('inorder'))
'''
'''
    def _insert(value, node):
        if node.left is None:
            node.left = Node(value)
        elif node.right is None:
            node.right = Node(value)
        else:
            node1=node
            size = Heap.size(node)
            level = math.floor(math.log(size+1)/math.log(2)- 1)
            offset = size - (2**(level+ 1)-1)
            maxi = 2**level
            if offset <= maxi/2:
                node1 = node.left
            else:
                node1 = node.right
            Heap._insert(value,node1)
'''
