'''
Name: Yusuf Ismaeel
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
        self.root = None
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
        if node is None:
            return True
        return AVLTree._balance_factor(node) in [-1,0,1] and AVLTree._is_avl_satisfied(node.left) and AVLTree._is_avl_satisfied(node.right)
        
        

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
        
        node1 = Node(node.right.value)
        node1.right = node.right.right
        
        leftNode = Node(node.value)
        leftNode.left = node.left
        leftNode.right = node.right.left
        
        node1.left = leftNode
        
        return node1
        

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
        
        node1 = Node(node.left.value)
        node1.left = node.left.left
        
        riteNode = Node(node.value)
        riteNode.right = node.right
        riteNode.left = node.left.right
        
        node1.right = riteNode
        
        return node1
        
    def insert_list(self,xs):
        for item in xs:
            self.insert(item)
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
            self.root = AVLTree._insert(value,self.root)

       
    
    @staticmethod
    def updateBalance(node):
        ''' 
        I got the idea and logic for the pseudocode for this balancing function from https://gist.github.com/girish3/a8e3931154af4da89995 and
        https://runestone.academy/runestone/books/published/pythonds/Trees/AVLTreeImplementation.html
        but then i had to adjust both so that they work for the way I'm coding it. 
        '''
        if AVLTree._balance_factor(node) > 1:
            if AVLTree._balance_factor(node.left)<0:
                node.left = AVLTree._left_rotate(node.left)
                return AVLTree._right_rotate(node)
            else:
                return AVLTree._right_rotate(node)
        elif AVLTree._balance_factor(node) < -1:
            if AVLTree._balance_factor(node.right) > 0:
                node.right = AVLTree._right_rotate(node.right)
                return AVLTree._left_rotate(node)
            else:
                return AVLTree._left_rotate(node)
        else: return node
  

    
    @staticmethod
    def _insert(value,node):
        '''This code follows essentially the same logic as the BST insert helper function but for this one i needed to rebalance my nodes
        Therefore, I created the helper function above to rebalance my nodes'''
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                AVLTree._insert(value,node.left)
        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                AVLTree._insert(value,node.right)
        else:
            print("Already in the tree")
            
        #All was well and dandy but this would not give me a balanced AVL tree so i have to balance within the insert helper function
        if AVLTree._is_avl_satisfied(node) == False:  #only do this if we are not balanced
            node.left = AVLTree.updateBalance(node.left) #rebalance the left node
            node.right = AVLTree.updateBalance(node.right) #rebalance the right node
            return AVLTree.updateBalance(node)     #return the whole balanced node
        else:
            return node
