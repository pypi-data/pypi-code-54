'''
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree file.
'''

from Trees.BinaryTree import BinaryTree, Node

class BST(BinaryTree):
    '''
    BST a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        super().__init__()
        self.root = None
        if xs:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a __str__ function,
        but not a __repr__ function.
        Recall that the __repr__ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's __repr__ will return "BST([1,2,3])"
        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST will have a correct implementation of __repr__,
        and that they won't have to reimplement it.
        '''
        return type(self).__name__+'('+str(self.to_list('inorder'))+')'


    def is_bst_satisfied(self):
        '''
        Whenever you implement a data structure,
        the first thing to do is to implement a function that checks whether
        the structure obeys all of its laws.
        This makes it possible to automatically test whether insert/delete functions
        are actually working.
        '''
        if self.root:
            return BST._is_bst_satisfied(self.root)
        return True

    @staticmethod
    def _is_bst_satisfied(node):
        '''
        Implement this method.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        If there is a node that has both a left and a right child,
        then the function will first recursively check the left node;
        then it returns before it checks the right node.
        '''
        left_valid = True
        right_valid = True

        if node.left:
            left_valid = node.value > node.left.value and BST._is_bst_satisfied(node.left)

        if node.right:
            right_valid = node.value < node.right.value and BST._is_bst_satisfied(node.right)

        return left_valid and right_valid


    def insert(self, value):
        '''
        Inserts value into the BST.
        '''
        if self.root is None:
            self.root = Node(value)
        else:
            BST._insert(value, self.root)


    @staticmethod
    def _insert(value, node):
        '''
        Implement this function.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                BST._insert(value, node.left)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                BST._insert(value, node.right)
        else:
            print("Value is already present in tree.")


    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        '''
        for x in xs:
            self.insert(x)


    def __contains__(self, value):
        return self.find(value)


    def find(self, value):
        '''
        Returns whether value is contained in the BST.
        '''
        if self.root:
            return BST._find(value, self.root)
        else:
            return False


    @staticmethod
    def _find(value, node):
        '''
        Implement this function.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
        if value > node.value and node.right:
            return BST._find(value, node.right)
        elif value < node.value and node.left:
            return BST._find(value, node.left)
        if value == node.value:
            return True




    def find_smallest(self):
        '''
        Returns the smallest value in the tree.

        Implement this function.
        This function is not implemented in the lecture notes,
        but if you understand the structure of a BST it should be easy to implement.
        HINT:
        Create a recursive staticmethod helper function,
        similar to how the insert and find functions have recursive helpers.
        '''
        if self.root:
            return BST._find_smallest(self.root)
        else:
            return None


    @staticmethod
    def _find_smallest(node):
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)


    def find_largest(self):
        '''
        Returns the largest value in the tree.

        Implement this function.
        This function is not implemented in the lecture notes,
        but if you understand the structure of a BST it should be easy to implement.
        '''
        if self.root:
            return BST._find_largest(self.root)
        else:
            return None


    @staticmethod
    def _find_largest(node):
        if node.right is None:
            return node.value
        else:
            return BST._find_largest(node.right)


    def remove(self,value):
        '''
        Removes value from the BST.
        If value is not in the BST, it does nothing.

        implement this function.
        There is no code given in any of the lecture videos on how to implement this function,
        but the video by HMC prof Colleen Lewis explains the algorithm.
        HINT:
        You must have find_smallest/find_largest working correctly
        before you can implement this function.
        HINT:
        Use a recursive helper function.
        '''
        self.root = BST._remove(self.root,value)


    @staticmethod
    def _remove(node,value):
        if node is None:
            return node
        if node.value > value:
            node.left = BST._remove(node.left, value)
        elif node.value < value:
            node.right = BST._remove(node.right, value)
        else:   # node.value == value

            # one child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # two children
            tmp = node.right
            while tmp.left:
                tmp = tmp.left
            node.value = tmp.value
            node.right = BST._remove(node.right, node.value)
        return node


    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.
        '''
        for x in xs:
            self.remove(x)

'''
bst = BST()
bst.insert(8)
bst.insert(3)
bst.insert(10)
bst.insert(1)
bst.insert(6)
bst.insert(9)
bst.insert(11)

# print(bst.find(11))
print(bst.print_tree('inorder'))
# print(bst.is_bst_satisfied())
# print(bst.find_largest())
print(bst.find_smallest())
print(bst.remove(8))
print(bst.print_tree('inorder'))

# tree = BST()
# tree.root = Node(1)
# tree.root.left = Node(2)
# tree.root.right = Node(3)
# tree.root.left.left = Node(-5)
# tree.root.left.right = Node(0)
# tree.root.right.left = Node(2)
# tree.root.right.right = Node(7)
# tree.root.right.right.right = Node(-8)
# print(tree.print_tree('inorder'))
# print(tree.is_bst_satisfied())
# print(tree.find_largest())
# print(tree.find_smallest())
'''
