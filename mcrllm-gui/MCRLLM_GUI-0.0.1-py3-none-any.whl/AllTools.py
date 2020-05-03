# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 10:10:16 2018
@author: cauh2701
"""
#from fct_MCRLLM import HyperspectralSegmentation_MCR_LLM
#from fct_MCRALS import HyperspectralSegmentation_MCR_ALS
#from init import *
#from tkinter import *
from tkinter.messagebox import showerror
from SI_File_Toolbox import loadFile, dataBin
import matplotlib.pyplot as plt
import numpy as np
from skimage.transform import resize
import dm4
import scipy.io as sc

def run(initList, fctList, nb_c, nb_iter, filepath, nb_dim, hier):
    for i in range(50):
        print("\n")
    
        
    x = loadFile(filepath)
        
   
    try:
        if nb_dim == 3:
        
            # resize image
            print(x.shape)  
            s0 = x.shape[0]
            s1 = x.shape[1]
            s2 = x.shape[2]
                
            nb_pix = s0*s1
        
            x = np.reshape(x, (nb_pix, s2))
            print('Image has been resized.')
            print(x.shape)
            
        elif nb_dim == 2:
            
            # resize image
            print(x.shape)  
            s0 = x.shape[0]
            s1 = 0
            s2 = x.shape[1]
            
        
            x = np.reshape(x, (s0, s2))
            print('Image has been resized.')
            print(x.shape)
        else:
            raise ValueError

    except ValueError:
        showerror('Erreur', 'Veuillez choisir un nombre de dimensions valide')
        return
    

    
    xraw = np.copy(x)
    

    list_to_plot = []
    
    for i in initList:
        
        if i.trigger:
            
            for f in fctList:
                
                check = 0
                
                if f.trigger:
                    
                    if (f.nom == 'PCA') or (f.nom == 'NMF'):
                        print("{}".format(f.nom))
                        
                        
                    else:
                        print("{} - {}".format(f.nom, i.nom))
                        
                        
                    try:
                        
                        obj = f.do(xraw, nb_c, init = i.nom , nb_iter = nb_iter)   #Appel de la fonction
                        [c, s] = obj.C , obj.S
                        C = np.array(c)
                        S = np.array(s)
                        
                            
                        list_to_plot.append([f,i,C,c,S,nb_c, nb_dim,s0,s1])
                        
                        check = 1
                        
                       
                    except:
                        
                        obj = f.do(xraw,nb_c)
                        [c, s] = obj.C , obj.S
                        C = np.array(c)
                        S = np.array(s)
                        
                        list_to_plot.append([f,i,C,c,S,nb_c, nb_dim,s0,s1])
                        check = 1
                        
                    
                    
                    if check == 0:
                        print("Non compatibles...")
                        break
                
                    
                    
                    
                    
    plot_hier = [] 

          
    if hier:      
    #Je ne savais pas comment appeler les fonctions d'initialisation et je n'avais pas le temps de l'apprendre, alors,
    #j'ai duck tapé ça un peu. Ça mériterait un clean up. On pourrait l'appeler comme les autres au lieu de la faire ici. Faut juste loader Sselect dans le fond
        su = np.load('data_PCA_select_X.npy')
            
        for f in fctList:
            
            if f.trigger:
                
                print("{} - {}".format(f.nom, 'Hiearchical'))
                try:

                    if (f.nom == 'MCR-LLM (full)') or (f.nom == 'MCR-LLM (half)') or (f.nom == 'MCR-ALS'):                    
                        obj = f.do(xraw, nb_c, init = su, nb_iter = nb_iter)   #Appel de la fonction
                        [c, s] = obj.C , obj.S 
                        C = np.array(c)
                        S = np.array(s)
                        
                        plot_hier.append([f,C,c,S,nb_c, nb_dim,s0,s1])
                            
                    else:
                        pass
                    
                    
                except ValueError:
                    print("Non compatibles...")
                    break
            
            
                
                
                
    for i in range(len(list_to_plot)):
        
        liste = list_to_plot[i]
        plot_spectra(liste[0] , liste[1] ,liste[2] ,liste[3] ,liste[4] ,liste[5] ,liste[6] ,liste[7] ,liste[8])
        
        
    for i in range(len(plot_hier)):
        
        liste = plot_hier[i]
        plot_spectra_hier(liste[0] , liste[1] ,liste[2] ,liste[3] ,liste[4] ,liste[5] ,liste[6] ,liste[7])
        
        
    stop()
   
  
    
    
    
def plot_spectra(f,i,C,c,S,nb_c, nb_dim,s0,s1):
    
    if (f.nom == 'PCA') or (f.nom == 'NMF'):
    
        plt.figure("Spectre {} / {} comp".format(f.nom, nb_c))
        leg = list()
    

        for iz in range(nb_c):
            leg.append("Elem {}".format(iz+1))
        
        for n in range (nb_c):
            plt.plot(S[n,:], linewidth = 0.7)
        
        plt.xlabel('Wavelength')
        plt.ylabel('Spectra')
        plt.title("{}".format(f.nom), fontsize=12)
        plt.legend(leg)
        plt.show()
    
      
    
    else:
        plt.figure("Spectre {} + {} / {} comp".format(f.nom, i.nom, nb_c))
    
        leg = list()
    
        for iz in range(nb_c):
            leg.append("Elem {}".format(iz+1))
        
        for n in range (nb_c):
            plt.plot(S[n,:], linewidth = 0.7)
        
        plt.xlabel('Wavelength')
        plt.ylabel('Spectra')
        plt.title("{} - {}".format(f.nom, i.nom), fontsize=12)
        plt.legend(leg)
        plt.show()
    
    
    
    if not isinstance(c, int): # Si c'est n'est pas un int => C'est un array
        
        if (f.nom == 'PCA') or (f.nom == 'NMF'):
            plt.figure("Chemical mapping {} / {} comp".format(f.nom, nb_c))
      
    
        else:
            plt.figure("Chemical mapping {} + {} / {} comp".format(f.nom, i.nom, nb_c))
        
        
        if  nb_dim == 3:
            
            C = np.reshape(C, (s0, s1, nb_c))
            for ic in range(nb_c):                        
                a = 331+ic
                plt.subplot(a); plt.imshow(C[:,:,ic])
                plt.title("Elem {}".format(ic+1))
                plt.colorbar()
                
                
        elif nb_dim==2:
            C = np.reshape(C, (s0, nb_c))
            plt.title("Concentrations")
            plt.xlabel('pixels')
            plt.ylabel('abondance')
            
            for ic in range(nb_c):                        
                plt.plot(C[:,ic])
                







def plot_spectra_hier(f,C,c,S,nb_c, nb_dim,s0,s1):
    
    
    plt.figure("Spectre {} + {} / {} comp".format(f.nom, 'Hiearchical', nb_c))


    leg = list()
    
    
    for iz in range(nb_c):
        leg.append("Elem {}".format(iz+1))
    
    for n in range (nb_c):
        plt.plot(S[n,:], linewidth = 0.7)
    
    plt.xlabel('Wavelength')
    plt.ylabel('Spectra')
    plt.title("{} - {}".format(f.nom, 'Hiearchical'), fontsize=12)
    plt.legend(leg)
    
    
    
    
    if not isinstance(c, int): # Si c'est n'est pas un int => C'est un array
    
        if (f.nom == 'PCA') or (f.nom == 'NMF'):
            plt.figure("Chemical mapping {} / {} comp".format(f.nom, nb_c))
      
    
        else:
            plt.figure("Chemical mapping {} + {} / {} comp".format(f.nom, 'Hiearchical', nb_c))
    
    
        if  nb_dim == 3:
            
            C = np.reshape(C, (s0, s1, nb_c))
            for ic in range(nb_c):                        
                a = 331+ic
                plt.subplot(a); plt.imshow(C[:,:,ic])
                plt.title("Elem {}".format(ic+1))
                plt.colorbar()
                
                
        elif nb_dim==2:
            C = np.reshape(C, (s0, nb_c))
            plt.title("Concentrations")
            plt.xlabel('pixels')
            plt.ylabel('abondance')
            
            for ic in range(nb_c):                        
                plt.plot(C[:,ic])
                
    
    

# Un peu broche à foin comme méthode, mais ca fonctionne
                
def stop():
    
    compteur = 0
    
    while True:
        
        if plt.waitforbuttonpress():
            compteur += 0
            
            if compteur == 10:
                break
        
        





                 

