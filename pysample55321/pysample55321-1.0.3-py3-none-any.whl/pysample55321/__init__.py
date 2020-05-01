import pyhellocpp

class Myobject(object):
    def __init__(self,txt):
        self.txt = txt
        
    def display(self):
        print ("MyObject Class")
        print(pyhellocpp.getGreetMsg(self.txt))
        print(pyhellocpp.getTime())
