# MCR ALS

"""
Coded by Jeffrey Byrns
Adapted by Ryan Gosselin
"""

# import packages
import numpy as np
from scipy import linalg
from SI_File_Toolbox import preprocess_data,final_process
from init import *



class HyperspectralSegmentation_MCR_ALS:
    
    
    def __init__(self,xraw, nb_c, init, nb_iter=50):  #I added xraw to facilitates call from GUI
    
        self.Xraw = xraw
        self.nb_c = nb_c
        
        self.X ,self.Xsum,self.deletedpix, self.deletedLevels, self.check_pix , self.check_level = preprocess_data(self.Xraw)
        
        
        x_n = np.sum(self.X, 1)
        x_n[x_n < 0.025*np.max(x_n)] = np.max(x_n)
        x = self.X.T / x_n
        self.X = x.T
        x.astype('float64')
        
        max_iter = 50

        self.define_initial_spectra(init)
        
        s = self.S

        cnt = 0
        flag = True
        
    
        while flag:
            s_mem = s

            # Concentrations by linear regression between X and S
            c1 = s @ s.T
            c2 = linalg.inv(c1)
            c3 = self.X @ s.T
            c = c3 @ c2

            c[c < 0] = 0
            c_sum = np.sum(c, 1) # Modification to C - Closure
            c_sum[c_sum == 0] = 1  # This line prevent any division by 0
            c = c.T / c_sum
            c = c.T


            # Spectra by linear regression between X and C
            s1 = c.T @ c
            s2 = linalg.inv(s1)
            s3 = c.T @ self.X
            s = s2 @ s3
            s[s < 0] = 0
            c_mem = c
            cnt = cnt + 1

            if cnt == max_iter or np.min(np.sum(s, 1)) == 0:
                if np.min(np.sum(s, 1)) == 0:
                    s = s_mem
                    c = c_mem
                flag = False


        self.C = c
        self.S = s

        self.C,self.S = final_process(self.C ,self.S, self.deletedpix , self.deletedLevels , self.check_pix , self.check_level )
        
        
        
    def define_initial_spectra(self,init):
    
        if type(init) == type(''):
            
            if init == 'Kmeans':
                print('Initializing with {}'.format(init))
                self.Sini = KmeansInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
                
            elif init == 'MBKmeans':
                print('Initializing with {}'.format(init))
                self.Sini = MBKmeansInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
            
            
            elif init == 'NFindr':
                print('Initializing with {}'.format(init))
                self.Sini = NFindrInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
            
            elif init == 'RobustNFindr':
                print('Initializing with {}'.format(init))
                self.Sini = RobustNFindrInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
                
            elif init == 'ATGP':
                print('Initializing with {}'.format(init))
                self.Sini = AtgpInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
               
            elif init == 'FIPPI':
                print('Initializing with {}'.format(init))
                self.Sini = FippiInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
                
            elif init == 'nKmeansInit':
                print('Initializing with {}'.format(init))
                self.Sini = nKmeansInit.initialisation(self.X,self.nb_c)
                self.S = self.Sini.copy()
        
        elif type(init) == type(np.array([1])):
            self.S = init
            
        else:
            raise('Initialization method not found')