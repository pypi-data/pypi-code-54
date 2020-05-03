# DEMI MCR LLM

"""
Coded by Jeffrey Byrns
Adapted by Ryan Gosselin
"""

# import packages
import numpy as np
from scipy.optimize import minimize
from functools import partial
from SI_File_Toolbox import preprocess_data,final_process
from init import *


class HyperspectralSegmentation_Demi_LLM:

       
    def __init__(self,xraw, nb_c , init , nb_iter):
        
        # We don't use the number of iterations, it is just to accomodate the GUI
        
        self.Xraw = xraw
        self.nb_c = nb_c
        
    
        self.X ,self.Xsum,self.deletedpix, self.deletedLevels, self.check_pix , self.check_level = preprocess_data(self.Xraw)
        
        if self.check_pix:
            self.Xraw = np.delete(self.Xraw , self.deletedpix , axis = 0)
            
            
        if self.check_level:
            self.Xraw = np.delete(self.Xraw , self.deletedLevels , axis = 1)
        
        
        self.define_initial_spectra(init)
        
        c_pred = self.X @ self.S.T @ np.linalg.inv(self.S @ self.S.T)
        
        c = self.C_plm(self.S, self.Xraw, nb_c, c_pred)
        
        self.C = c
        
        self.C,self.S = final_process(self.C ,self.S, self.deletedpix , self.deletedLevels , self.check_pix , self.check_level )
    
    
    
    
    
    def C_plm(self, s, xraw, nb_c, c_pred):
        #initialize C

        [nb_pix,nb_lev] = np.shape(xraw)
        c_new = np.zeros((nb_pix,nb_c))
        


        # on calcule les concentrations optimales pour chaque pixel par maximum likelihood 
        for pix in range(nb_pix):

                x_sum = np.sum(xraw[pix,:])      #total des counts 
                sraw = s*x_sum
                
                c_new[pix,:] = self.pyPLM(nb_c, sraw, xraw[pix,:], c_pred[pix,:])
                
                
         # avoid errors (this part should not be necessary)
        c_new[np.isnan(c_new)] = 1/nb_c
        c_new[np.isinf(c_new)] = 1/nb_c
        c_new[c_new<0] = 0
        c_sum1 = np.array([np.sum(c_new,axis=1)])
        c_sum =c_sum1.T@np.ones((1,np.size(c_new,axis =1)))
        c_new = c_new/c_sum

        return c_new
    
    
    
    def pyPLM(self, nb_c, sraw, xrawPix, c_old):
        

        # sum of every value is equal to 1
        def con_one(c_old):
            return 1-sum(c_old) 
        

        # all values are positive
        bnds = ((0.0, 1.0),) * nb_c
        

        cons = [{'type': 'eq', 'fun': con_one}]
        
        
        
        
        def regressLLPoisson(sraw,  xrawPix, c_pred):
            
            
            
            #compute prediction of counts
            yPred = c_pred @ sraw
            
            # avoid errors, should not be necessary
            yPred[yPred < 1/(10000*len(yPred))] = 1/(10000*len(yPred))
            
            
            
            
            logLik = -np.sum(xrawPix*np.log(yPred)-yPred)
            
            
            return (logLik)
        
        
        
        def jacobians(nb_c, xrawPix, sraw, c_pred):

            #compute prediction of counts
            yPred = c_pred @ sraw
            
            
            #compute jacobians
            jacC = np.zeros(nb_c)
            
            for phase in range(nb_c):
                
                jacC[phase] = -np.sum(((xrawPix*sraw[phase,:])/yPred)-sraw[phase,:])
                
            return(jacC) 
        

   
                
        # Run the minimizer    
        results = minimize(partial(regressLLPoisson, sraw,  xrawPix), c_old, method='SLSQP', bounds=bnds, constraints=cons, jac = partial(jacobians, nb_c, xrawPix, sraw))
        results = results.x
        results = np.asarray(results)
        


        c_new = results.reshape(int(len(results) / nb_c), nb_c)
        
        
        return c_new
    
    
    

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