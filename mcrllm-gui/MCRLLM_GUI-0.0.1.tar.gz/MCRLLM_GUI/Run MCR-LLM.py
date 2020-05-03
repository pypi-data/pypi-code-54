# -*- coding: utf-8 -*-
"""
@auteurs : Louis-Philippe Baillargeon, Hugo Caussan et Yannick Poulin-G.
"""
#%% User Input
from init import KmeansInit as ini                                  # Choose the initialization to use1
from fct_MCRALS import HyperspectralSegmentation_MCR_ALS            # Import the algorithm to use
from MCRLLM import mcrllm   # This one is from the pypi
from MCR_LLM_new import mcrllm_new
from fct_PCA import PCA,Center,optimal_scaling


# CHOOSE THE ALGORITHM 

Algorithm_PCA = True
Algorithm_MCR_ALS = False 
Algorithm_MCR_LLM =  False
Algorithm_MCR_LLM_NEW = False

# SET THE PARAMETERS

#paramètres d'affichage (only necessary for vms file)
Emin = 199.5                # énergie du niveau 0 eV
Emax = 600                  # énergie du niveau max eV
step = 0.5                  # Écart entre les niveaux d'énergie
pas = 1                     # distance entre les pixels (nm)

#file parameters
path = 'data1.npy'          # choose your file
dim = 3                         # 2D or 3D file
nb_c = 4                        # Number of components(phases)

#analysis parameters - general
Bin = False                     # Bin the data
correctPix = False              # Enable the cosmic Xray filter, only works with sufficient dwell time
nb_etype = 3                    # Criteria for cosmic Xray

#analysis parameters - mcrllm 
nb_i = 10                       # Number of iterations in mcr_llm


#%% Code
import numpy as np
from SI_File_Toolbox import loadFile, dataBin, normalize
from cosmicRays import findWeirdPixels, estimateWeirdPixelsList
import matplotlib.pyplot as plt


# LOAD THE DATA

print("load data")  

X3 = loadFile(path,Emin,Emax,step)


if dim == 3:
    dim1 = X3.shape[0]
    dim2 = X3.shape[1]
    nb_level = X3.shape[2]
    nb_pix = dim1*dim2
    
    
elif dim == 2:
    nb_level = X3.shape[1]
    nb_pix = X3.shape[0]


X = np.reshape(X3, (nb_pix, nb_level))


# Bin the data set
        
if Bin:
    print("\nbin data :")     
    X = dataBin(X, 2)


# Deal with weird pixels

# Finds the corrputed by Xray energy levels of a pixel by comparing it to the same levels of other pixels. If its too large, it is approximated by an average of its neigbours
# Only works with high count data
    
if correctPix:
    print("\nDeal with weird pixels:")     
    Xtrash = np.copy(X)
    
    print("\nfind weird pixels:")    
    weirdlev, weirdmap = findWeirdPixels(np.copy(X), nb_etype)

    
    print("\nestimate weird pixels:")    #partie un peu longue, pourrait améliorer   
    X = estimateWeirdPixelsList(np.copy(X), weirdlev, weirdmap, neighbours = 3)
    
    
    
#%%
#avoid errors, if an energy level has 0 counts on all pixels, it causes log(0) and the level is meaningless, so we take it out

nb_level_deleted = 0

x_sum = np.sum(X, axis = 0)

deletedLevels = np.where(x_sum <= 0)[0]

X1 = np.delete(X, deletedLevels, axis = 1)
    
nb_level_deleted = len(deletedLevels)


#np.seterr(divide = 'ignore' , invalid = 'ignore')

#%%

#We take out the pixels which did not receive any counts

nb_pix_deleted = 0

x_sum = np.sum(X1, axis = 1)

deletedpix = np.where(x_sum <= 0)[0]

X2 = np.delete(X1, deletedpix, axis = 0)
    
nb_pix_deleted = len(deletedpix)
    

#%%
    
Xraw = np.copy(X2)
X_norm = normalize(X2)


#%% Initilisation (necessary for MCR-ALS and MCR-LLM)

if (Algorithm_MCR_ALS == True) or (Algorithm_MCR_LLM == True):
    print("Initialisation :")
    Si = ini.initialisation(Xraw, nb_c) # Initialisation


#%%
    
    
if Algorithm_MCR_LLM == True:

    print("MCR LLM : " + str(nb_c) + " composantes - " + str(nb_i) +" itérations\n")
    C, S = mcrllm(Xraw, nb_c, init = Si, nb_iter = nb_i) # Algorithm
    
    
if Algorithm_MCR_LLM_NEW == True:
    
    print("MCR LLM NEW : " + str(nb_c) + " composantes - " + str(nb_i) +" itérations\n")
    code = mcrllm_new(Xraw , nb_c , method = 'normal')
    code.iterate(nb_i)
    C,S  = code.C ,code.S
    
    
if Algorithm_MCR_ALS == True :
    
    print("MCR ALS : " + str(nb_c) + " composantes - " + str(nb_i) +" itérations\n")
    C, S = HyperspectralSegmentation_MCR_ALS.mcr_als(Xraw, nb_c, Si, nb_i) # Algorithm



if Algorithm_PCA == True:
    
    print('Centering')
    X_Centered = Center(Xraw)
    
    print('Optimal scaling')
    X_scaled = optimal_scaling(X_Centered)
    
    print("PCA : " + str(nb_c) + ' composantes ')
    C, S , SSX = PCA(X_scaled, nb_c) # Algorithm
    



#%%
    
#Insert deleted spectra back (the spectra was 0 that's why we took it out) and deleted pixels

for i in range(nb_level_deleted):
    
    S_final = np.insert(S,deletedLevels[i], np.zeros(nb_c), axis = 1)
    

#%%

# Add back the pixels which we took out
    
C_final = np.zeros([nb_pix,nb_c])
compteur = 0

for i in range(nb_pix):
    
    if np.any(deletedpix == i):
        
        C_final[i,:] = 0
        compteur += 1
    
    else: 
        C_final[i,:] = C[i-compteur,:]
    

#%% Show the results
    
from SI_File_Toolbox import plotCompare, plotSpectraGroup


#rearrange data
if dim == 3:
    C3 = np.reshape(C_final, (dim1,dim2, nb_c))
    plotCompare(S, Emin, Emax, C3, pas = 1, log = False)
    
else:
    plt.figure()
    plt.plot(C)


plotSpectraGroup(S, np.arange(nb_c), Emin = Emin, Emax = Emax)


