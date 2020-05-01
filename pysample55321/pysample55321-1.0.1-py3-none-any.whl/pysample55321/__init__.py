class Myobject(object):
    def __init__(self,txt):
        self.txt = txt
        
    def display(self):
        print ("MyObject Class")
        print ("-> {0}".format(self.txt))
