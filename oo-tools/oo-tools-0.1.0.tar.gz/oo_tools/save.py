import os, pathlib, pickle

class Saver:
    
    """
    Save your object to a file location. Use this object as a base class for another.
    """
    
    @property
    def filepath(self):
        """Filepath of where you want to save the object.
        
        Returns:
            str -- filepath
        """
        try:
            return self._filepath
        except:
            raise FileNotFoundError('You didn\'t specify the filepath of the object to save!')
            
    @filepath.setter
    def filepath(self, filepath):
        """Set the filepath. For exmaple/var/lib/mytest.obj
        
        Arguments:
            filepath {str} -- filepath or location where you want to save the object with teh file name
        
        Raises:
            IOError: The directory doesn't exist
            AttributeError: No suffix supplied, like .obj
        """
        fp = pathlib.Path(filepath)
        
        if not os.path.exists(fp.parent):
            # check the directory
            raise IOError(f'Directory = {fp.parent} does not exist! Create it first')
        
        if not fp.suffix:
            # check that there's a suffix
            raise AttributeError(f'You must supply a suffix to the filepath. For example, "/this/path/test.obj", not {filepath}')
        
        self._filepath = filepath
    
    def save(self):
        """save the object
        """
        with open(self.filepath, 'wb') as f:
            pickle.dump(self.__dict__, f, 2)
            f.close()
    
    def load(self):
        """Load the object
        """
        with open(self.filepath, 'rb') as f:
            tmp_dict = pickle.load(f)
            self.__dict__.update(tmp_dict)

            f.close()