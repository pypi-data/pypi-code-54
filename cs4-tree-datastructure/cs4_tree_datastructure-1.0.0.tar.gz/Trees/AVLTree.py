'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree and BST files.
'''

from Trees.BinaryTree import BinaryTree, Node
from Trees.BST import BST

class AVLTree(BST):
    '''
    FIXME:
    AVLTree is currently not a subclass of BST.
    You should make the necessary changes in the class declaration line above 
    and in the constructor below.
    '''

    def __init__(self, xs=None):
        '''
        FIXME:
        Implement this function.
        '''
        super().__init__()
        if xs:
            self.insert_list(xs)

    def balance_factor(self):
        '''
        Returns the balance factor of a tree.
        '''
        return AVLTree._balance_factor(self.root)

    @staticmethod
    def _balance_factor(node):
        '''
        Returns the balance factor of a node.
        '''
        if node is None:
            return 0
        return BinaryTree._height(node.left) - BinaryTree._height(node.right)


    def is_avl_satisfied(self):
        '''
        Returns True if the avl tree satisfies that all nodes have a balance factor in [-1,0,1].
        '''
        return AVLTree._is_avl_satisfied(self.root)

    @staticmethod
    def _is_avl_satisfied(node):
        '''
        FIXME:
        Implement this function.
        '''
        correct = [-1, 0, 1]
        if node is None:
            return True
        else:
            return AVLTree._is_avl_satisfied(node.right) and AVLTree._is_avl_satisfied(node.left) and AVLTree._balance_factor(node) in correct

    @staticmethod
    def _left_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        if node is None or node.right is None:
            return node

        newRoot = Node(node.right.value)
        newRoot.right = node.right.right
        newRoot.left = Node(node.value)
        newRoot.left.left = node.left
        newRoot.left.right = node.right.left

        return newRoot

    @staticmethod
    def _right_rotate(node):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of tree rotations,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.
        '''
        if node is None or node.left is None:
            return node

        newRoot = Node(node.left.value)
        newRoot.left = node.left.left
        newRoot.right = Node(node.value)
        newRoot.right.right = node.right
        newRoot.right.left = node.left.right

        return newRoot
    def insert(self, value):
        '''
        FIXME:
        Implement this function.

        The lecture videos provide a high-level overview of how to insert into an AVL tree,
        and the textbook provides full python code.
        The textbook's class hierarchy for their AVL tree code is fairly different from our class hierarchy,
        however, so you will have to adapt their code.

        HINT:
        It is okay to add @staticmethod helper functions for this code.
        The code should look very similar to the code for your insert function for the BST,
        but it will also call the left and right rebalancing functions.
        '''
        def _insert(node):
            if value < node.value:
                if node.left is None:
                    node.left = Node(value)
                else:
                    node.left = _insert(node.left)
            elif value > node.value:
                if node.right is None:
                    node.right = Node(value)
                else:
                    node.right = _insert(node.right)
                    
            node = AVLTree._rebalance(node)
            return node

        if self.root is None:
            self.root = Node(value)
        else:
            self.root = _insert(self.root)

    @staticmethod
    def _rebalance(node):
        balance_difference = AVLTree._balance_factor(node)

        if balance_difference in [-2, -1, 0, 1, 2]:
            if balance_difference < 0:
                if AVLTree._balance_factor(node.right) > 0:
                    node.right = AVLTree._right_rotate(node.right)
                    node = AVLTree._left_rotate(node)

                else:
                    node = AVLTree._left_rotate(node)
            elif balance_difference > 0:
                if AVLTree._balance_factor(node.left) < 0:
                    node.left = AVLTree._left_rotate(node.left)
                    node = AVLTree._right_rotate(node)
                else:
                    node = AVLTree._right_rotate(node)
            return node
        else:
            return False
