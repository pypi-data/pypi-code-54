# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 15:28:17 2018

@author: cauh2701
"""

import numpy as np
from sklearn.decomposition import NMF
from SI_File_Toolbox import preprocess_data,final_process
from init import *

class HyperspectralSegmentation_NMF:
    
    
    def __init__(self, xraw, nb_c, nb_iter = 50):
        
        
        self.Xraw = xraw
        self.nb_c = nb_c
        self.X ,self.Xsum,self.deletedpix, self.deletedLevels, self.check_pix , self.check_level = preprocess_data(self.Xraw)
    
        
        model = NMF(n_components=nb_c, max_iter=nb_iter, init='random', random_state=0)
        s = model.fit_transform(self.X.T)
        
        
        s = s.T
        c = self.X @ s.T @ np.linalg.inv(s @ s.T)
        
        
        self.C = c
        self.S = s
        
        self.C,self.S = final_process(self.C ,self.S, self.deletedpix , self.deletedLevels , self.check_pix , self.check_level )
        
        
        

