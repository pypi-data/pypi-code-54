'''

Author : Ryan Gosselin and Yannick Poulin-Giroux 

'''

import numpy as np
from SI_File_Toolbox import preprocess_data,final_process
from init import *

    
class PCA_segmentation:
    
    def __init__(self,Xraw, nb_PC):
        
        self.Xraw = Xraw
        self.nb_PC = nb_PC
        
        #We firt normalize spectra by their sum. We take out energy levels and pixels with 0 count 
        self.X ,self.Xsum,self.deletedpix, self.deletedLevels, self.check_pix , self.check_level = preprocess_data(self.Xraw)
        
        
        # We center data
        print('Centering X')
        m = np.array([np.mean(self.X, axis=0)])
        X_center = self.X - m
        
        
        # We execute a scalling best on the recommandations un Francis' paper
        print('Optimal scalling X')
        X_opti = self.optimal_scaling(X_center)
        
        
        #We run PCA NIPALS
        print('PCA with {} principal components'.format(self.nb_PC))
        self.C , self.S = self.PCA(X_center , self.nb_PC)
        
        
        # We reverse the optimal scalling
        Xpca = self.reverse_optimal_scaling(self.C@self.S)
        
        
        # We uncenter the data matrix reconstituaded by PCA
        Xpca = Xpca + m
        
        
        # We get our final spectra 
        self.S = np.linalg.inv(self.C.T@self.C)@self.C.T@Xpca
        
        
        # We add back the pixel and levels deleted if there were any
        self.C,self.S = final_process(self.C ,self.S, self.deletedpix , self.deletedLevels , self.check_pix , self.check_level )
        
    
    
    
    
    # Method of scaling based on the recommandations in Francis' paper 
    
    def optimal_scaling(self,Xraw):
        
        X_scaled = np.copy(Xraw)
        
        np.seterr(divide = 'ignore' , invalid = 'ignore')
        
        mean_level = np.sqrt(np.mean(Xraw , axis = 1))
           
        mean_pix = np.sqrt(np.mean(Xraw , axis = 0))
        
        self.mean_level = mean_level
        self.mean_pix = mean_pix
        
        if np.any(mean_level == 0):
            print('Zeros met in the mean of some pixels spectra')
            
        if np.any(mean_pix == 0):
            print('Zeros met in the mean of some energy levels')
        
        for i in range(len(Xraw[:,0])):
            
            for j in range(len(Xraw[0,:])):
                
                X_scaled[i,j] = Xraw[i,j]/(mean_level[i] * mean_pix[j])
         
            
        # Should not be necessary because pixels and level with 0 count on them were taken out 
        if np.any(X_scaled != X_scaled):
            
            eq = 1/len(Xraw[0,:])
            X_scaled = np.where(X_scaled != X_scaled, eq, X_scaled)
                
        
        return X_scaled
    
    
    
    def reverse_optimal_scaling(self,Xpca):
        
        X_final = np.copy(Xpca)
        
        for i in range(len(Xpca[:,0])):
            
            for j in range(len(Xpca[0,:])):
                
                X_final[i,j] = Xpca[i,j]*(self.mean_level[i] * self.mean_pix[j])
        
        
        return X_final
    
    
    def PCA(self,X, nbPC):
        
        
        s0, s1 = X.shape
        T = np.zeros((s0, nbPC))
        P = np.zeros((s1, nbPC))
        SSX = np.zeros((nbPC, 1))
        X0 = X # Save a copy
        
        
        for i in range(0,nbPC):
            error = 10
            t_temp = np.ones((s0, 1))
            t = np.ones((s0, 1))
            
            compteur = 0
            
            while error > 1E-10:
                p = (X.T@t)/(t.T@t)
                p = p/np.linalg.norm(p,2)
                # np.linalg.norm(p,2) = np.max(np.sqrt(p.T @ p))
                t = (X@p)/(p.T@p)
                # Check t convergence --------------------
                error = sum(np.power((t-t_temp),2),0) # Squared error
                t_temp = t
                
                compteur += 1
                
                if compteur == 1500 :
                    
                    if input('PCA meets difficulties to find de lasts components. Want to continu (y) or stop (n) ? ') == 'y':
                        break
    
                # ----------------------------------------     
            P[:,i] = np.squeeze(p)
            T[:,i] = np.squeeze(t)
            X = X - t@p.T
            
            # Sum of squares -----------
            Xhat = t@p.T
            ssX0 = np.sum(np.sum(X0 * X0)) # Each element squared
            ssX = np.sum(np.sum(Xhat * Xhat))
            ssX = ssX / ssX0
            SSX[i] = ssX
            # --------------------------
            
        return T, P.T




            
            
    


