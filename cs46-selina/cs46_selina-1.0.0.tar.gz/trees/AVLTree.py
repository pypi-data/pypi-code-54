'''
This file implements the AVL Tree data structure.
The functions in this file are considerably harder than the functions in the BinaryTree and BST files.
'''

from Trees.BinaryTree import BinaryTree, Node
from Trees.BST import BST

class AVLTree(BST):
	def __init__(self, xs=None):
		super().__init__()
		if xs:
			self.insert_list(xs)

	def balance_factor(self):
        	return AVLTree._balance_factor(self.root)

	@staticmethod
	def _balance_factor(node):
		if node is None:
	    		return 0
		return BinaryTree._height(node.left) - BinaryTree._height(node.right)


	def is_avl_satisfied(self):
        	return AVLTree._is_avl_satisfied(self.root)

	@staticmethod
	def _is_avl_satisfied(node):
		if node is None:
			return True
		return AVLTree._balance_factor(node) in [-1, 0, 1] and AVLTree._is_avl_satisfied(node.left) and AVLTree._is_avl_satisfied(node.right)

   
	@staticmethod
	def _left_rotate(node):
		if node is None or node.right is None:
			return node
		newroot = Node(node.right.value)
		newroot.right = node.right.right
		
		new_left = Node(node.value)
		new_left.left = node.left
		new_left.right = node.right.left
		newroot.left = new_left
		return newroot


	
	@staticmethod
	def _right_rotate(node):
		if node is None or node.left is None:
			return node	
		newroot = Node(node.left.value)
		newroot.left = node.left.left
		
		new_right = Node(node.value)
		new_right.right = node.right
		new_right.left = node.left.right
		newroot.right = new_right
		return newroot
		

	def insert(self, value):
		if self.root is None:
			self.root = Node(value)
		else:
			self.root = AVLTree._insert(value, self.root)

            
	def insert_list(self, xs):
		for x in xs:
			self.insert(x)


	@staticmethod
	def _insert(value,node):
		if value < node.value:
			if node.left is None:
				node.left = Node(value)
			else:
				AVLTree._insert(value, node.left)
		elif value > node.value:
			if node.right is None:
				node.right = Node(value)
			else:
				AVLTree._insert(value, node.right)
		else:
			print('Already in the tree')

		if AVLTree._is_avl_satisfied(node) == False:
			node.left = AVLTree.rebalance(node.left)
			node.right = AVLTree.rebalance(node.right)
			return AVLTree.rebalance(node)
		else:
			return node


	@staticmethod
	def rebalance(node):
		if AVLTree._balance_factor(node)> 1:
			if AVLTree._balance_factor(node.left) < 0:
				node.left = AVLTree._left_rotate(node.left)
			return AVLTree._right_rotate(node)
		elif AVLTree._balance_factor(node)<-1:
			if AVLTree._balance_factor(node.right)>0:
				node.right = AVLTree._right_rotate(node.right)
			return AVLTree._left_rotate(node)
		else:
			return node


