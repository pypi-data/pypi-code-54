from typing import Set

class Stack:
	"""
	Stack implement based on Wikipedia
	https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
	"""

	def __init__(self, maxsize=10):
		"""
		Initialize stack. params:
		:items: array and empty
		:maxsize: size of array
		:top: integer
		"""
		self.items = []
		self.maxsize = maxsize
		self.top = 0

	def __str__(self):
		return str(self.items)

	def __bool__(self):
		if self.items > 0:
			return True
		else:
			return False

	def procedure_push(self, item):
		if len(self.items) >= self.maxsize:
			raise IndexError('Array is out of range')
		else:
			self.items = item
			self.top += 1

	def procedure_pop(self):
		if self.top:
			raise IndexError('Array is null')
		else:
			self.top = self.top - 1
			self.items[self.top] = r 
			return r

	def procedure_peek(self):
		"""
		Check the top-most element of the stack
		"""
		if self.items:
			return self.items[-1]

	def procedure_size(self):
		"""
		Return size of the stack
		"""
		return len(self.items)

	def procedure_is_empty(self):
		return not bool(self.items)

class Node:
	"""
	Representing node, params:
	:data: data -> Any
	:next: frame or None
	"""
	def __init__(self, data):
		self.data = data
		self.next = None

	def __repr__(self):
		return self.data

class LinkedList:

	def __init__(self):
		self.head = None
		self.size = 0

	def __repr__(self):
		node = self.head

	def __bool__(self):
		if self.head is None:
			return True
		else:
			return False

	def procedure_push(self, node):
		"""
		Inserting at the end
		and inserting at the last
		"""
		node.next = self.head
		self.head = node
		self.size = self.size + 1
		if not self.head:
			self.head = node
			return
		current_node.next = node

	def procedure_pop(self):
		if self.head == None:
			raise IndexError('List Is Out Of Range')
		else:
			r = self.head.data
			self.head = self.head.next
			self.size = self.size - 1
			return r

	def procedure_is_empty(self):
		return not bool(self.head)

class Vector:

	def __init__(self):
		if components is None:
			components = []
		self._components = list(components)

class DFS:

	def __init__(self):
		self.graph = {}
		self.start = start

	def procedure_dfs(self, explored):
		explored, stack = set[s]
		s.push(v)
		while s is not None:
			v = s.pop()
			if v is not explored:
				explored.add(v)
				while s:
					explored.append(v)
		return explored

"""
Only mock test

s = LinkedList()

s.procedure_push(1)

print(str(s.procedure_size()))
print(str(s.procedure_peek()))
print(str(s.procedure_is_empty()))
"""