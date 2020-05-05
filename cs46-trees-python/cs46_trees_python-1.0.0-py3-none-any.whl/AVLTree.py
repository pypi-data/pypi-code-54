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
            for x in xs:
                self.insert(x)

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
        if AVLTree._balance_factor(node) not in [-1,0,1]:
            return False
        if node: 
            if node.left and node.right:
                return AVLTree._is_avl_satisfied(node.left) and AVLTree._is_avl_satisfied(node.right)
            if node.left and node.right is None: 
                return AVLTree._is_avl_satisfied(node.left)
            if node.right and node.left is None: 
                return AVLTree._is_avl_satisfied(node.right)
        return True
        
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

        new_root = Node(node.right.value)
        new_root.right = node.right.right

        new_left = Node(node.value)
        new_left.left = node.left
        new_left.right = node.right.left

        new_root.left = new_left

        return new_root

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
        '''
        new_root = node.left
        temp = node.left.right

        new_root.right = node
        node.left = temp 

        return new_root
        '''

        if node is None or node.left is None:
            return node 

        new_root = Node(node.left.value)
        new_root.left = node.left.left

        new_right = Node(node.value)
        new_right.right = node.right
        new_right.left = node.left.right 

        new_root.right = new_right

        return new_root 

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
        if self.root is None:
            self.root = Node(value)
        else: 
            self.root = AVLTree._insert(self.root,value)

    @staticmethod
    def _insert(node,value): 
        '''
        insert helper function

        P.S. I used the following logic https://www.geeksforgeeks.org/avl-tree-set-1-insertion/ and modified accordingly
        '''
        
        if node is None: 
            return Node(value)
        elif value < node.value:
            node.left = AVLTree._insert(node.left, value)
        else:
            node.right = AVLTree._insert(node.right,value)
        
        balance = AVLTree._balance_factor(node)

        #Left Left
        if balance > 1 and value < node.left.value:
            return AVLTree._right_rotate(node)
        #Right Right
        if balance < -1 and value > node.right.value: 
            return AVLTree._left_rotate(node)
        #Left Right
        if balance > 1 and value > node.left.value:
            node.left = AVLTree._left_rotate(node.left)
            return AVLTree._right_rotate(node)
        #Right Left
        if balance < -1 and value < node.right.value:
            node.right = AVLTree._right_rotate(node.right)
            return AVLTree._left_rotate(node)

        return node







avl = AVLTree()
avl.root = Node(0)
avl.root.left = Node(-2)
avl.root.left.left = Node(-3)
avl.root.left.left.left = Node(-4)
avl.root.left.left.left.left = Node(-5)
avl.root.left.right = Node(-1)
avl.root.right = Node(2)
avl.root.right.left = Node(1)
avl.root.right.right = Node(3)
avl.root.right.right.right = Node(4)
