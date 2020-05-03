# -*- coding: utf-8 -*-
"""
@auteurs :  Hugo Caussan, Louis-Philippe Baillargeon et Yannick Poulin-G. 
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.io import savemat
import dm4
import scipy.io as sc
import scipy.stats as st
from collections import Counter
from matplotlib import cm

#import pypng as png

"""Ce script contient des fonctions utiles pour travailler avec des spectres images""" 



# Sert à ouvrir les plots à l'exterieur de la console
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass

# Permet d'ouvrir un fichier dm3 / Mat / spd
def loadFile(filepath, Emin=0, Emax=0 , step = 0):

    if filepath[-4:]==".dm4":
        dm4data = dm4.DM4File.open(filepath)
        tags = dm4data.read_directory()
        image_data_tag = tags.named_subdirs['ImageList'].unnamed_subdirs[1].named_subdirs['ImageData']
        image_tag = image_data_tag.named_tags['Data']
        dim1 = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[0])
        dim2 = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[1])
        nb_level = dm4data.read_tag_data(image_data_tag.named_subdirs['Dimensions'].unnamed_tags[2])
        x = np.array(dm4data.read_tag_data(image_tag), dtype=np.uint16)
        x = np.reshape(x, (dim1,dim2,nb_level), order = 'F')    #shape the matrix like the data is stored
    
    elif filepath[-4:]==".mat":#Load a Mat file 
        Xdict = sc.loadmat(filepath)
        x = Xdict['image_round']
        
    elif filepath[-4:]==".txt":#Load a txt file 
        x = np.loadtxt(filepath, comments="#", delimiter=",", unpack=False).T
    
    elif filepath[-4:]==".spd": # SPD FILE (EDAX)
        h = open(filepath,'rb')
        header = {}
        header['tag'] = np.fromfile(h,'int8',16)
        header['version'] = np.fromfile(h,'int32',1)[0]
        header['nSpectra'] = np.fromfile(h,'int32',1)[0]
        header['nCols'] = np.fromfile(h,'int32',1)[0]
        header['nRows'] = np.fromfile(h,'int32',1)[0]
        header['nChannels'] = np.fromfile(h,'int32',1)[0]
        header['countBytes'] = np.fromfile(h,'int32',1)[0]
        header['dataOffset'] = np.fromfile(h,'int32',1)[0]
        header['nFrames'] = np.fromfile(h,'int32',1)[0]
        header['fName'] = np.fromfile(h,'int8',120)
        header['filler'] = np.fromfile(h,'int8',900)
        x = np.zeros([header['nSpectra'],header['nChannels']],'int16')
        for i in range(0,header['nSpectra']):
            x[i,:] = np.fromfile(h,'int16',header['nChannels'])
        h.close()
        x = np.float64(x)
        x = np.reshape(x,[header['nRows'],header['nCols'],header['nChannels']])
        
    elif filepath[-4:]==".npy": # SPD FILE (EDAX)
        x = np.load(filepath)
        
    
    
    # Ajout non-optimal pour faire la lecture d'un vms, il est mieux de convertir le fichier en .mat
    
    elif filepath[-4:] == '.vms':
        data = pd.read_csv(filepath, ';' , header = None , engine = 'python')
     
        nb_image = int((Emax-Emin)/step)

        header = 16
        useless_spacing = 56
        end_mark = 0
        image_lenght = 256**2

        x = np.zeros([nb_image,image_lenght])
        X = np.zeros([256,256 , nb_image])
        count = []


        for i in range(0,nb_image):
    
            begin = header + useless_spacing*(i+1) + image_lenght*i
            stop = header + useless_spacing*(i+1) + image_lenght*i + image_lenght  + end_mark -1
    
    
            a = data.iloc[begin:stop , 0]
            a = a.to_numpy().astype(float)
            
    
            for j in range(len(a)):
        
                x[i,j] = float(a[j])
                count.append(float(a[j]))
            
            X[:,:,i] = np.reshape(x[i] , [256,256])
    
            if i == (nb_image - 2):
                end_mark = 1 
            
        print("Voici une dictionnaire détaillant l'occurence de chaque valeur de count dans le jeux de données: ")   
        print(Counter(np.array(count)))
        print('\nLa moyenne de count/pix/image est de {0:3.3f}'.format(np.sum(np.array(count))/(nb_image*image_lenght)))
        
        
        element_left = len(data) - (header + useless_spacing*(i+1) + image_lenght*(i+1) + end_mark)
        
        print('\nElement left in the data imported : ' + str(element_left) + '  (supposed to be 0)')

        x = X
        
    else:
        print("Type de fichier "+filepath[-4:]+" non prix en charge!" )

    return x











def preprocess_data(xraw):
    
    x_sum = np.sum(xraw, axis=1)
    xcopy = np.copy(xraw)
    check_pix = False
    check_level = False
    deletedpix = 0
    deletedLevels = 0
    
    
    
    
    #we take out every pixels which did not receive any count. We will add them back at the end 
    
    if np.any(x_sum == 0):
        
        print('One or more pixel(s) did not receive any count so they were taken out for the calculation')
            
        check_pix = True
        deletedpix = np.where(x_sum == 0)[0]
        xcopy = np.delete(xraw, deletedpix, axis = 0)
        x_sum = np.delete(x_sum , deletedpix)
        
    
    
    
    #Avoid errors, if an energy level has 0 counts on all pixels, it causes log(0) and the level is meaningless, so we take it out
    
    sum_level = np.sum(xcopy , axis = 0)
    
    if np.any(sum_level == 0):
        
        print('One or more level of energy did not have any count on it so they were taken out for calculation')
        check_level = True
        
        deletedLevels = np.where(sum_level == 0)[0]
        
        xcopy = np.delete(xcopy , deletedLevels , axis = 1 )
        


    
    #We finally normalize each spectra so their sum is zero
        
    x_sum = np.array([np.sum(xcopy, axis=1)]).T
    x = xcopy / x_sum
    
  
    return x , x_sum , deletedpix , deletedLevels , check_pix , check_level
    






def final_process(C, S , deletedpix , deletedLevels, check_pix, check_level):
    
    
    nb_c = np.shape(C)[1]
    
    # We add back the pixels we took out initially. The concentrations are all set to 0

    if check_pix == True:
        
        nb_pix_ori = np.shape(C)[0] + len(deletedpix)
        
        
        C_final = np.zeros([nb_pix_ori, nb_c])
        
        counter = 0
            
        
        for i in range(nb_pix_ori):
            
            if np.any(deletedpix == i):
                
                C_final[i,:] = 0
                counter += 1
            
            else: 
                C_final[i,:] = C[i-counter,:]
                
    
    else:
        C_final = C
    
    
    
    
    #Insert deleted levels back 
    
    if check_level == True:
        
        nb_level_ori = np.shape(S)[1] + len(deletedLevels)
        
        S_final = np.zeros([nb_c , nb_level_ori] )

        counter = 0
            
        
        for i in range(nb_level_ori):
            
            if (i-counter) >= (np.shape(S)[1] - 1) :
                
                S_final[:,i] = S[:, np.shape(S)[1] - 1]
            
            
            elif np.any(deletedLevels == i):
                
                S_final[:,i] = (S[:,i-counter-1] + S[:,i-counter+1])/2
                counter += 1
                
            
            else: 
                S_final[:,i] = S[:,i-counter]
                
        
    else:
        S_final = S
                
        
        
        
    return C_final,S_final
        






# Verify if a distribution is indeed poisson
def poissonVerify(X):
# X must be a np.array set of pixels of same specie of form [pix,lev]
    Xvar = np.var(X, axis = 0)
    Xmean = np.mean(X, axis = 0)
    slope, intercept, r_value, p_value, std_err = st.linregress(Xvar,Xmean)
    
    plt.figure()
    plt.xlabel('Variance', fontsize = 25)
    plt.ylabel('Mean', fontsize = 25)
    plt.plot(Xvar, Xmean)
    plt.plot()
    ax = plt.axes()
    x = np.linspace(0, np.max(Xvar), 1000)
    ax.plot(x, intercept + slope*x);
    
    print('slope : ' + str(slope))
    print('r : ' + str(r_value))
    
    return slope, r_value, intercept


    

# Permet de bin une image spectrale
def dataBin(x, n = 2):
    dim = len(x.shape)
    if dim == 2:
        s0 = x.shape[0]
        s0 = s0 - s0%n
        
        xb = np.zeros((int(s0/n), x.shape[1]))
        for i in range(n):
            f = range(i,s0,n)
            xb = xb + x[f,:]
        
    elif dim == 3:
        s0 = x.shape[0]
        s1 = x.shape[1]
        
        s0 = s0 - s0%n
        s1 = s1 - s1%n
        
        x = x[:s0,:s1,:]
        xb = np.zeros((int(s0/n),int(s1/n),x.shape[2]))
        
        for i in range(n):
            f1 = range(i,s0,n)
            for j in range(n):
                f2 = range(j,s1,n)
                xb = xb + x[f1,:,:][:,f2,:]
        
    return xb/(n**(dim-1))


# Generate everything but the data on a plot
def plotSpectraSetup(title, xlabel, ylabel):     
    plt.figure()           
    plt.title(title, fontsize = 25)
    plt.xlabel(xlabel, fontsize = 25)
    plt.ylabel(ylabel, fontsize = 25)
    plt.tick_params(axis='both',length=12,which='both',labelsize='large')
    #plt.grid(True)

     
# Plot the spectra for all phases
def plotSpectra(S, Emin = 0, Emax = 20, title = 'Phase spectra', xlabel = 'eV', ylabel = 'Abundance (/1)'):
    x = np.linspace(Emin,Emax, S.shape[1])            
    for i in range (S.shape[0]):
            plotSpectraSetup(str(title)+ ' ' + str(i), str(xlabel), str(ylabel))
            plt.plot(x, S[i])
            
# Plot the spectra of a few phases on the same plot to facilitate comparison, group is a np array that contains the indices of the phases that are meant to be ploted together
def plotSpectraGroup(S, group, Emin = 0, Emax = 20):
    x = np.linspace(Emin,Emax, S.shape[1])       
    plotSpectraSetup("Multiple phase Spectra", "eV", "Abundance (%)")
    
    for i in range(len(group)):
        plt.plot(x, 100*S[group[i],:])
        

            
# Plot les cartes de concentration de toutes les phases only works with 3D
def Cmap(cf):

    for i in range(0, len(cf[0,0,:])):
        plt.figure()
        plt.title('Concentration de la phase '+str(i))
        plt.imshow(np.log(cf[:,:,i]))
        plt.show()

# Plot Cmaps and spectras on one page
# If log is set to true, log concentrations will be shown instead of concentrations. Usefull if contrast is small, but can create false impression of high differences.
def plotCompare(S, Emin, Emax, C, pas = 1, log = False, title  = 'Phase '):
    x = np.linspace(Emin,Emax, S.shape[1])  
    
    for i in range (S.shape[0]):

        plt.figure()
        
        #spectra
        plt.subplot(1,2,1)
        #plt.xlabel('loss (eV)', fontsize = 25)
        #plt.ylabel('abundance', fontsize = 25)
        #plt.tick_params(axis='both',length=12,which='both',labelsize='large') 
        plt.plot(x, S[i,:], '-', lw=2)
        #plt.title(title + str(i) + ' Spectra', fontsize = 25)
        #plt.grid(True)
        
        
        #conc
        plt.subplot(1,2,2)
        plt.tick_params(axis='both',length=12,which='both',labelsize='large')
        
        if log:
            plt.imshow(np.log(C[:,:,i]), origin = 'lower' , cmap = 'inferno')
            
        else:
            plt.imshow(C[:,:,i], origin = 'lower' , cmap ='inferno')
        #plt.xlabel('pixels', fontsize = 25)
        #plt.ylabel('pixels', fontsize = 25)
        #plt.title(title + str(i) + ' concentration map', fontsize = 25)
        #plt.grid(True)
        plt.colorbar(orientation = 'horizontal')
        plt.show
        



# plot le spectre total (tous les niveaux d'énergie additionnés)          
def spectraMap(X3D):   #X3D sous forme[YDim,XDim,Elevel]
    X2D = np.sum(X3D, axis = 2)
    plt.figure()
    plt.title('Tout le spectre reçu')
    plt.imshow(np.log(X2D.T), origin = 'lower')
    plt.show()
    
    
def importMJdata(path):
#Fonction spécifique au données simulées EDX 10 pyramides, elles sont enregistrées sousla forme X3[nb_level, xdim, ydim]
    X3= loadFile(path)
    X3 = X3.T
    return X3

    
        


                
                
                
                
                
                

    