# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 11:32:50 2019

@author: Louis-Philippe Baillargeon et Yannick Poulin-Giroux 
"""

import numpy as np
from sklearn import decomposition
from fct_pointselector import SelectFromCollection
from SI_File_Toolbox import plotSpectra
import matplotlib.pyplot as plt
from fct_pointselector import Score_plot_3D


def computeShow(S_hier, nb_c, Emin = 0, Emax = 20):
#Computes the PCA and opens the windows to select wanted spectra
    
    #substract mean for pca
    Smoy = np.mean(S_hier, axis = 1)
    S_centered = S_hier.T-Smoy
    S_centered = S_centered.T
    
    #pca transformation
    pca = decomposition.PCA(n_components=nb_c)
    pca.fit(S_centered)
    
    components = pca.components_
    plotSpectra(components, Emin = Emin, Emax = Emax, title = 'Principal Component', ylabel = 'score')
        
    return 






def computeSelect(S_hier, nb_pc):
#Computes the PCA and opens the windows to select wanted spectra
    
    #substract mean for pca
    Smoy = np.mean(S_hier, axis = 1)
    S_centered = S_hier.T-Smoy
    S_centered = S_centered.T
    
    #pca transformation
    pca = decomposition.PCA(n_components=nb_pc)
    pca.fit(S_centered)
    
    Spca = pca.transform(S_centered)  # spectra expressed in principal components
    
    Sselect = [SelectFromCollection(Spca, S_hier)]
    print('More phases : enter 1  Else enter 0')
    morePhase = int(input())
    nb_c = 1
    
    while(1):
    
        Sselect = np.append(Sselect,[SelectFromCollection(Spca, S_hier)])
        print('More phases : enter 1   Else enter 0')
        morePhase = int(input())
        nb_c = nb_c +1
        if morePhase == 0:
            break
    
    return Sselect, nb_c
    






def interactive_selection(S_H, nb_phases):

    
    #S_H = np.load('data_H.npy')
    print('Hierarchical spectra: ',S_H.shape)
        
    # Center and scale to unit variance
    S_H_mean = np.mean(S_H,axis=0)
    S_H_std = np.std(S_H,axis=0)
    S_H = (S_H - S_H_mean)/S_H_std
    
    #PCA
    # Number of PCA components
    nb_pc = int(input('\nNumber of principal components for PCA \n(Should be equal or superior to your number of chemical species)  :  '))
    pca = decomposition.PCA(n_components=nb_pc)
    pca.fit(S_H)
    
    Spca = pca.transform(S_H)  # spectra expressed in PCA scores (t)
    
    
    a = input('Want a 3D score plot before selecting (y/n) ? ')
    
    plt.ion()
    
    if a == 'y':
        
        unsatisfied = True
        
        while unsatisfied: 
            
            plot = Score_plot_3D(Spca)
        
            while True:
            
                if plot.accepted == True:
                    unsatisfied = False
                    break
                    
                plt.pause(1)  
    
    plt.ioff()
    
    # Number of reference spectra to be found in PCA score space
    print('\n####################\n')
    print('\nCreate reference spectra based on the hierarchical spectra obtained.')
    print('To do so:')
    print('1. You will be asked to select as many spectra as you have chemical species ')
    print('2. Each time, you will choose the PCA scores to plot with (usually t1 and t2) ')
    print('3. Circle with your mouse 1 or more spectra to be combined into a reference spectra')
    print("4. Accept the spectra presented with 'enter' or re-do the selection until satisfication")
    
    plt.ion()
    
    Final_spectra = np.zeros([nb_pc-1,len(S_H_mean)])
    
    
    for i in range(nb_phases):
        
        Sselect = SelectFromCollection(Spca, S_H, S_H_mean, S_H_std)
    
        while True:
        
            if Sselect.accepted == True:
                a = Sselect.ind
                Select = np.mean(S_H[a,:],axis=0)
                #Stored spectra are uncenterd and unscaled
                Final_spectra[i,:] = Select*S_H_std + S_H_mean
                break
        
            plt.pause(1)
        
    
    plt.ioff()
    
    np.save('data_PCA_select_X.npy', Final_spectra)
        
    #print('\nSpectra are saved in file : data_PCA_select_X.npy')
    
    
