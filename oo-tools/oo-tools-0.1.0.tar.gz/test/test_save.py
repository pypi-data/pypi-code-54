import unittest

from oo_tools.save import Saver

import os

class TestSaver(unittest.TestCase):
    def setUp(self):
        self.saver = Saver()
        self.filepath = '/tmp/test.obj'
        
    def tearDown(self):
        try:
            os.remove(self.filepath)
        except:
            pass
    
    def test_set_filepath(self):
        
        # test didn't set suffix
        with self.assertRaises(AttributeError):
            self.saver.filepath = '/tmp/test'
    
        # test invalid directory
        with self.assertRaises(IOError):
            self.saver.filepath = '/blah/test'
        
        # test valid path works
        self.saver.filepath = self.filepath
        assert self.saver.filepath
        
    def test_save(self):
        # throws if no path is set
        with self.assertRaises(FileNotFoundError):
            self.saver.save()

        # it saves
        self.saver.filepath = self.filepath
        self.saver.save()
        
        assert os.path.isfile(self.filepath)
    
    def test_load(self):
        
        # mock class used for testing
        class SomeObj(Saver):
            def __init__(self):
                self.stuff = 'hello'
        
        # make sure it saves the current state of the object
        someobj = SomeObj()
        
        someobj.filepath = self.filepath
        someobj.stuff = 'different'
        
        someobj.save()
        assert os.path.isfile(self.filepath)
        
        del someobj
        
        new_someobj = SomeObj()
        assert new_someobj.stuff == 'hello'
        
        new_someobj.filepath = self.filepath
        new_someobj.load()
        
        assert new_someobj.stuff == 'different'
        
                
        
        
        