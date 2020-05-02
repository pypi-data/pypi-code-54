'''
This file implements the Binary Search Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree file.
'''

from Trees.BinaryTree import BinaryTree, Node, Stack

class BST(BinaryTree, Node):
    '''
    FIXME:
    BST is currently not a subclass of BinaryTree.
    You should make the necessary changes in the class declaration line above 
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        If xs is a list (i.e. xs is not None),
        then each element of xs needs to be inserted into the BST.
        '''
        self.root = None
        if xs:
            self.insert_list(xs)

    def __repr__(self):
        '''
        Notice that in the BinaryTree class,
        we defined a _str_ function,
        but not a _repr_ function.
        Recall that the _repr_ function should return a string that can be used to recreate a valid instance of the class.
        Thus, if you create a variable using the command BST([1,2,3])
        it's _repr_ will return "BST([1,2,3])"
        For the BST, type(self).__name__ will be the string "BST",
        but for the AVLTree, this expression will be "AVLTree".
        Using this expression ensures that all subclasses of BST will have a correct implementation of _repr_,
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
            print(BST._is_bst_satisfied(self.root))
            return BST._is_bst_satisfied(self.root)
        return True

    @staticmethod
    def _is_bst_satisfied(node):
        '''
        FIXME:
        Implement this method.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
        if node.value == None:
            return True
        if node.left and node.right:
            if node.value < node.right.value and node.value > node.left.value:
                return BST._is_bst_satisfied(node.left) and BST._is_bst_satisfied(node.right) 
            else:
                return False      
        if node.left:
            if node.value > node.left.value:
                return BST._is_bst_satisfied(node.left)
            else:
                return False
        if node.right:
            if node.value < node.right.value:
                return BST._is_bst_satisfied(node.right)
            else:
                return False
        return True
        
            

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
        FIXME:
        Implement this function.
        The lecture videos have the  exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
                node.left.parent = value
            else:
                BST._insert(value, node.left)

        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
                node.right.parent = node
            else:
                BST._insert(value, node.right)
        else:
            print("Value already in tree!")


    def insert_list(self, xs):
        '''
        Given a list xs, insert each element of xs into self.
        FIXME:
        Implement this function.
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
        FIXME:
        Implement this function.
        The lecture videos have the exact code you need,
        except that their method is an instance method when it should have been a static method.
        '''

        if value > node.value and node.right: 
            return BST._find(value,node.right)
        elif value < node.value and node.left:
            return BST._find(value,node.left) 
        if value == node.value:
            return True
        else:
            return False

    
    @staticmethod
    def _find_node(value, node):
        '''
        requires that value is already in tree with node as the root
        '''
        if value > node.value and node.right: 
            return BST._find_node(value,node.right)
        elif value < node.value and node.left:
            return BST._find_node(value,node.left) 
        if value == node.value:
            return node



    def find_smallest(self):
        '''
        Returns the smallest value in the tree.
        FIXME:
        Implement this function.
        This function is not implemented in the lecture notes,
        but if you understand the structure of a BST it should be easy to implement.
        HINT:
        Create a recursive staticmethod helper function,
        similar to how the insert and find functions have recursive helpers.
        '''
        node = self.root
        return BST._find_smallest(node).value
        
    
    @staticmethod
    def _find_smallest(node):
        if node.left is not None:
            return BST._find_smallest(node.left)
        else:
            return node


    def find_largest(self):
        '''
        Returns the largest value in the tree.
        FIXME:
        Implement this function.
        This function is not implemented in the lecture notes,
        but if you understand the structure of a BST it should be easy to implement.
        '''
        node = self.root
        return BST._find_largest(node).value
        
    
    @staticmethod
    def _find_largest(node):
        if node.right is not None:
            return BST._find_largest(node.right)
        else:
            return node


    def remove(self,value):
        '''
        Removes value from the BST. 
        If value is not in the BST, it does nothing.
        FIXME:
        implement this function.
        There is no code given in any of the lecture videos on how to implement this function,
        but the video by HMC prof Colleen Lewis explains the algorithm.
        HINT:
        You must have find_smallest/find_largest working correctly 
        before you can implement this function.
        HINT:
        Use a recursive helper function.
        '''
        
        self.root = BST._remove(value,self.root)
        
    @staticmethod
    def _remove(value, node):
        if node==None:
            return None
        if not node.left and not node.right:
            if node.value==value:
                return None
            else:
                return node
            
        if node.left and not node.right:
            if node.value==value:
                return node.left
            else:
                node.left=BST._remove(value,node.left)
                return node
            
        if node.right and not node.left:
            if node.value==value:
                return node.right
            else:
                node.right=BST._remove(value,node.right)
                return node
        
        if node.left and node.right:
            if node.value==value:
                sm_right=BST._find_smallest(node.right)
                sm_right.left=node.left
                return node.right
            else:
                if value < node.value:
                    node.left=BST._remove(value,node.left)
                    return node
                else:
                    node.right=BST._remove(value,node.right)
                    return node

    def remove_list(self, xs):
        '''
        Given a list xs, remove each element of xs from self.
        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.remove(x)
