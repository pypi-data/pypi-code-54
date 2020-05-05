from Trees.BinaryTree import BinaryTree, Node


class BST(BinaryTree):
    def __init__(self, xs = None): 
       super().__init__()
       if xs:
           self.insert_list(xs)
    
    def __repr__(self):
        return type(self).__name__+'('+str(self.to_list('inorder'))+')'
            
    def is_bst_satisfied(self): 
    #    if self.root:
           # is_satisfied = self._is_bst_satisfied(self.root)

          #  if is_satisfied is None:
         #       return True 
        #    return False
        
       # return True

        if self.root:
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

        is_left_satisfied=True
        is_right_satisfied = True 

        if node.left:
            if node.value > node.left.value:
                is_left_satisfied = BST._is_bst_satisfied(node.left)
            else:
                is_left_satisfied =  False

        if node.right:
            if node.value < node.right.value:
                is_right_satisfied =  BST._is_bst_satisfied(node.right)
            else:
                is_right_satisfied = False

        return is_left_satisfied and is_right_satisfied


    def insert(self,value):
        """Inserts value into the BST"""
        if self.root is None:
            self.root = Node(value)
        else:
            BST._insert(value, self.root)
    
    @staticmethod
    def _insert(value,node):
        if value < node.value :
            if node.left is None:
                node.left = Node(value)
            else:
                BST._insert(value,node.left)

        elif value > node.value:
            if node.right is None:
                node.right = Node(value)
            else:
                BST._insert(value,node.right)
            
    def insert_list(self,xs): 
        '''
        Given a list xs, insert each element of xs into self.
        FIXME:
        Implement this function.
        '''
        for x in xs:
            self.insert(x)
    
    def __contains__(self,value):
        return self.find(value)
    
    def find(self, value):
        if self.root:
            if BST._find(value,self.root):
                return True 
        else: 
            return False 
    
    @staticmethod
    def _find(value,node):
        if value > node.value and node.right:
            return BST._find(value,node.right)
        
        elif value < node.value and node.left:
            return BST._find(value, node.left)
        
        if value == node.value:
            return True   

        else:
            return False
    
    def find_smallest(self): 
        if self.root.left is None:
            return self.root.value 
        else:
            return BST._find_smallest(self.root)
        
    @staticmethod
    def _find_smallest(node):
        if node.left is None:
            return node.value
        else:
            return BST._find_smallest(node.left)
            
    def find_largest(self):
        if self.root.right is None:
            return self.root.value
        else:
            return BST._find_largest(self.root)
    
    @staticmethod
    def _find_largest(node):
        if node.right is None:
            return node.value 
        else:
            return BST._find_largest(node.right)
    
    def remove(self,value): 
        self.root = BST._remove(self.root,value)



    @staticmethod
    def _remove(node,value):
        if node is None:
            return
        if value > node.value:
            node.right = BST._remove(node.right, value)
        elif value < node.value:
            node.left = BST._remove(node.left, value)
        else:
            #first case = no subtrees
            if node.right is None and node.left is None:
                return None
            #second case = one subtree
            if node.right and node.left is None:
                return node.right
            if node.left and node.right is None:
                return node.left 
            #third case = two subtree 
            node.value = BST._find_smallest(node.right)
            node.right = BST._remove(node.right, node.value)
        return node 





       # if node.right:
          #  if node.right.value == value:
            #Case three
              #  if node.right and node.right.value == value and node.right.left and node.right.right:
                  #  store_right = BST._find_smallest(node.right.right)
                 #   BST._remove(node.right, store_right)
                #    node.right.value = store_right
            #Case two 
               # if node.right and node.right.value == value and (node.right.left or node.right.right):
               #     if node.right.left:
              #          node.right.value = node.right.left.value
             #           node.right.left = None
            #        if node.right.right:
           #             node.right.value = node.right.right.value
          #              node.right.right = None
            #Case one
         #       if node.right and node.right.value == value:
        #            node.right == None


       # if node.left:
           # if node.left.value == value:
            #Case three    
               # if node.left and node.left.value == value and node.left.left and node.left.right:
              #      store_left = BST._find_largest(node.left.left)
             #       BST._remove(node.left, store_left)
            #        node.left.value = store_left 
            #Case two 
           #     if node.left and node.left.value == value and (node.left.left or node.left.right):
          #          if node.left.left:
         #               node.left.value = node.left.left.value
        #                node.left.left = None
       #             if node.left.right:
      #                  node.left.value = node.left.right.value 
     #                   node.left.right = None
            #Case one 
    #            if node.left and node.left.value == value:
   #                 node.left == None

  #      if value > node.value and node.right:
 #           return BST._remove(node.right, value)
#        elif value < node.value and node.left:
    #        return BST._remove(node.left, value)

    def remove_list(self,xs): 
         for x in xs:
            self.remove(x)
            

