# -*- coding: utf-8 -*-
"""
@auteurs: Hugo Caussan et Louis-Philippe Baillargeon
"""

# import packages
import numpy as np
from scipy.optimize import minimize
import scipy.stats as stats
from functools import partial
from tqdm import tqdm
from scipy.special import factorial
from SI_File_Toolbox import preprocess_data,final_process
from init import *


 
class mcrllm:
    
    
    def __init__(self,Xraw,nb_c,init,nb_iter=1,method="variable",fact_ini=.5):
        
        # Save Xraw and normalize data
        self.Xraw = Xraw
        self.X ,self.Xsum,self.deletedpix, self.deletedLevels, self.check_pix , self.check_level = preprocess_data(self.Xraw)
        
        if self.check_pix:
            self.Xraw = np.delete(self.Xraw , self.deletedpix , axis = 0)
            
        if self.check_level:
            self.Xraw = np.delete(self.Xraw , self.deletedLevels , axis = 1)
            
        
        self.pix,self.var = np.shape(self.X)
        self.nb_c = nb_c
        self.method = method 
        self.expvar = np.inf
        self.fact_ini = fact_ini
        
        # History initialization
        self.allC = []
        self.allS = []
        self.allphi = []
        
        
        self.C = np.ones([self.pix,self.nb_c])/nb_c
        

            
        # Initialization
        self.define_initial_spectra(init)
        
        
        
        for iteration in range(nb_iter):
            print("Iteration {:.0f}".format(len(self.allS)+1))

            
            self.C_plm()
            self.S_plm()
            
            
        self.C,self.S = final_process(self.C ,self.S, self.deletedpix , self.deletedLevels , self.check_pix , self.check_level )
        
        
     
    
    def C_plm(self):
        
        c_new = np.zeros((self.pix,self.nb_c))
        

        # on calcule les concentrations optimales pour chaque pixel par maximum likelihood 
        for pix in range(self.pix):
            sraw = self.S*self.Xsum[pix]
            c_new[pix,:] = self.pyPLM(sraw, self.Xraw[pix,:], self.C[pix,:])
                
                
        # avoid errors (this part should not be necessary)
        c_new[np.isnan(c_new)] = 1/self.nb_c
        c_new[np.isinf(c_new)] = 1/self.nb_c
        c_new[c_new<0] = 0
        c_sum1 = np.array([np.sum(c_new,axis=1)]).T
        c_new = c_new/c_sum1

        self.C = c_new.copy()
        self.allC.append( c_new.copy() )
    
            
        
        
    
    def Sphi(self,phi,h):
    
        C_m = self.C**phi
            
        S = np.linalg.inv(C_m[h,:].T@C_m[h,:])@C_m[h,:].T@self.X[h,:]
        S[S<1e-15] = 1e-15
        S = S/np.array([np.sum(S,axis=1)]).T
        
        return S
    
    
    
    
    def S_plm(self):
        
        
        h = np.random.permutation(len(self.X))
        phi_optimal = 1
        
        if self.method == "variable":
            allMSE = []
            all_phis = np.arange(.1,10.1,.1)
            
            for phi in all_phis:
                S = self.Sphi(phi,h)
                allMSE.append(np.sum( (S-self.S)**2 ))
                
            phi_optimal = all_phis[np.argmin(allMSE)]
            self.S = self.Sphi(phi_optimal,h)
            
            
                    
        else: # Standard
            
            self.S =  self.Sphi(phi_optimal,h)
            
            
        self.allS.append( self.S.copy() )
        self.allphi.append(phi_optimal)
        
        
        
    
    
    def pyPLM(self, sraw, xrawPix, c_old):
        

        # sum of every value is equal to 1
        def con_one(c_old):
            return 1-sum(c_old) 
        
        
        
        def regressLLPoisson(sraw,  xrawPix, c_pred):
            
            #compute prediction of counts
            yPred = c_pred @ sraw
            nb_lev = len(yPred) #
            # avoid errors, should (may?) not be necessary
            yPred[yPred < 1/10000] = 1/10000
            logLik = -np.sum(xrawPix*np.log(yPred)-yPred)
            return (logLik)
        
        
        
        def jacobians(nb_c, xrawPix, sraw, c_pred):

            #compute prediction of counts
            yPred = c_pred @ sraw
            # avoid errors, should (may?) not be necessary
            yPred[yPred < 1/10000] = 1/10000
            
            #compute jacobians
            jacC = np.zeros(nb_c)
            
            for phase in range(nb_c): 
                jacC[phase] = -np.sum(((xrawPix*sraw[phase,:])/yPred)-sraw[phase,:])    
            return(jacC) 
        
        
        
        # all values are positive
        bnds = ((0.0, 1.0),) * self.nb_c
        cons = [{'type': 'eq', 'fun': con_one}]
   
                
        # Run the minimizer    
        results = minimize(partial(regressLLPoisson, sraw,  xrawPix), c_old,\
                           method='SLSQP', bounds=bnds, constraints=cons, \
                           jac = partial(jacobians, self.nb_c, xrawPix, sraw))
        results = np.asarray(results.x)
        

        c_new = results.reshape(int(len(results) / self.nb_c), self.nb_c)
        
        
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
        







