#!/usr/bin/env python3

#######################################################################
# Copyright (c) 2019, Quasar Astronomy Group.
# Produced at Lawrence Berkeley National Laboratory.
# Written by V. Dumont (vincentdumont11@gmail.com).
# All rights reserved.
# For details, see gitlab.com/astroquasar/research/whitedwarf.
# For details about use and distribution, please read LICENSE.
#######################################################################

# Import packages
import os,numpy,math,matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator,FixedLocator
from scipy.ndimage import gaussian_filter1d
from qsotools import spec,voigt,zoom

# Define speed of light
speedLight=299792.458

# Clean customized matplotlib settings from GwPy
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
# Use seaborn plotting style
plt.style.use('seaborn')
# Set up plotting details
plt.rc('font', size=13, family='sans-serif')
plt.rc('axes', labelsize=13, linewidth=0.2)
plt.rc('legend', fontsize=12, handlelength=2)
plt.rc('xtick', labelsize=13)
plt.rc('ytick', labelsize=13)
plt.rc('lines', lw=0.2, mew=0.2)
#plt.rc('grid', linewidth=0.5)

# Initialize figure
fig = plt.figure(1,figsize=(12,8))
plt.subplots_adjust(left=0.05, right=0.94, bottom=0.1, top=0.9, hspace=0.1, wspace=0.1)

# Create wavelength array
R    = 20000.
fwhm = 17.#speedLight/R
disp = fwhm/(2*numpy.sqrt(2*math.log(2)))
wave = [1100]
while wave[-1]<1500:
    wave.append(wave[-1]*(2*speedLight+disp)/(2*speedLight-disp))
numpy.savetxt('wave.dat', numpy.transpose([wave, numpy.ones_like(wave), numpy.ones_like(wave), ]))

# Prepare RDGEN input commands to generate artificial spectrum
N,b,z = 13.3,8,0
script = open('./commands.dat','w')
script.write('rd wave.dat \n')
script.write('gp \n')
script.write('H2I %f %f %f \n'%(N,b,z))
script.write('\n')
script.write('%f \n'%fwhm)
script.write('noise \n')
script.write('\n')
script.write('10\n')
script.write('wt spec.dat (all)\n')
script.write('lo\n')
script.close()

# Execute RDGEN with input commands
os.system('rdgen < commands.dat > termout')
os.system('rm termout')

# Load atomic and spectral data
H2I   = numpy.loadtxt('atom.dat',usecols=(1,2,3),dtype=float)
H2I   = H2I[H2I[:,0].argsort()]
data  = numpy.loadtxt('spec.dat')
wave  = data[:,0]
flux  = data[:,1]
error = data[:,2]
prof  = data[:,3]

xmin=1340
xmax=1360

# Plot whole spectrum
print('|- Plot whole spectrum...')
ax1 = fig.add_subplot(4,1,1,xlim=[wave[0],wave[-1]],ylim=[-0.2,1.4])
ax1.axvspan(xmin,xmax,color='blue',alpha=0.1,lw=0)
ax1.plot(wave,flux,color='black')
ax1.plot(wave,error,color='black',ls='dotted',alpha=0.5,lw=0.8)
ax1.xaxis.tick_top()
ax1.xaxis.set_label_position('top') 
ax1.yaxis.set_major_locator(plt.FixedLocator([0,1]))
plt.xlabel(r'Wavelength ($\mathrm{\AA}$)')

# Plot part of the spectrum
print('|- Plot part of the spectrum...')
ax2 = fig.add_subplot(4,1,2,ylim=[-0.2,1.4])
ax2.step(wave*(2*speedLight+disp/2)/(2*speedLight-disp/2),flux,color='black')
ax2.plot(wave,error,color='black',ls='dotted',alpha=0.5,lw=0.8)
ax2.plot(wave,prof,color='red',alpha=0.5,lw=1)
#ax2.xaxis.tick_top()
ax2.xaxis.set_tick_params(labelsize=10)
ax2.xaxis.set_major_locator(plt.FixedLocator([1342.5,1345,1347.5,1350,1352.5,1355,1357.5]))
ax2.tick_params(axis='x', pad=1.5)
ax2.yaxis.set_major_locator(plt.FixedLocator([0,1]))
#plt.setp(ax2.get_xticklabels(), visible=False)
plt.xlim(xmin,xmax)
zoom.zoom_effect01(ax1, ax2, xmin,xmax)

# Add tick marks for each H2 component
for i in range(len(H2I)):
    ax2.plot([H2I[i,0],H2I[i,0]],[1.2,1.3],color='red',lw=0.6)

# Combine each molecular line
n,pos = 0,[17,18,19,20,21,25,26,27,28,29]

# Look for 10 strongest lines in zoomed in region
temp = H2I[ (H2I[:,0]>xmin) * (H2I[:,0]<xmax) ]
temp = temp[temp[:,1].argsort()][::-1]
regs = numpy.empty((0,3))
for i in range(len(temp)):
    if True in (abs(2 * (regs[:,0]-temp[i,0]) / (regs[:,0]+temp[i,0]) * speedLight)<75):
        continue
    else:
        regs = numpy.vstack((regs,temp[i]))

# Colar span 10 strongest line region
for wstrong in regs[:10,0]:
    wmin = wstrong * (2*speedLight-75) / (2*speedLight+75)
    wmax = wstrong * (2*speedLight+75) / (2*speedLight-75)
    ax2.axvspan(wmin,wmax,color='blue',alpha=0.1,lw=0)
    ax2.text(wstrong,-0.1,'H2 %.2f'%wstrong,ha='center',va='bottom',color='blue',fontsize=8,alpha=0.8,rotation=90)

# Plot stacked H2 transition
print('|- Plot stacked molecular line')
ax3 = plt.subplot2grid((4,8),(2,5),rowspan=2,colspan=3,xlim=[-75,75],ylim=[0.9,1])
    
# Loop through all H2 transitions
print('|- Combine molecular line...')
for i in range(len(H2I)):

    # Combine transition to previous lines
    #print('{0:>5} / {1:<5}'.format(i+1,len(H2I)))
    wmin  = H2I[i,0]-10
    wmid  = H2I[i,0]
    wmax  = H2I[i,0]+10
    imin  = abs(wave-wmin).argmin()
    imax  = abs(wave-wmax).argmin()
    if i==0:
        wave0 = wave[imin:imax]
        data  = spec.rebin(wave0,flux[imin:imax],error[imin:imax],wa=wave0)
    else:
        zmid  = H2I[0,0]/wmid-1
        wave1 = wave[imin:imax]*(zmid+1)
        rebin = spec.rebin(wave1,flux[imin:imax],error[imin:imax],wa=wave0)
        data  = spec.combine([data,rebin])

    if i in [500,800,1000,1500]:
        zlist = data.wa/H2I[0,0]-1
        vlist = (((zlist+1)**2-1)/((zlist+1)**2+1))*speedLight
        ax3.plot(vlist,data.fl,label='%i lines'%i,lw=0.5)
    
    # Plot ten transition regions
    if H2I[i,0] in regs[:10,0]:

        velocity = 2*(wave[imin:imax]-wmid)/(wave[imin:imax]+wmid)*speedLight
        ax = fig.add_subplot(4,8,pos[n],xlim=[-75,75],ylim=[-0.2,1.4])
        ax.plot(velocity,prof[imin:imax],color='red',alpha=0.5,lw=1)
        ax.step(velocity+disp/2,flux[imin:imax],color='black')
        ax.text(0,0.1,'H2 %.2f'%H2I[i,0],ha='center',va='bottom',fontsize=12,alpha=0.8)
        ax.xaxis.set_major_locator(plt.FixedLocator([-50,0,50]))
        ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))

        # Add tick marks for each H2 component
        for i in range(len(temp)):
            velocity = 2*(temp[i,0]-wmid)/(temp[i,0]+wmid)*speedLight
            ax.plot([velocity,velocity],[1.2,1.3],color='red',lw=0.6)
        
        if pos[n] not in [17,25]:
            plt.setp(ax.get_yticklabels(), visible=False)
        if pos[n] in [17,18,19,20,21,22]:
            plt.setp(ax.get_xticklabels(), visible=False)
        if pos[n]==27:
            plt.xlabel(r'Velocity dispersion (km/s)')
        n += 1

zlist = data.wa/H2I[0,0]-1
vlist = (((zlist+1)**2-1)/((zlist+1)**2+1))*speedLight
ax3.plot(vlist,data.fl,color='black',lw=1,label='%i lines (full stack)'%len(H2I))
ax3.xaxis.set_major_locator(plt.FixedLocator([-50,-25,0,25,50]))
ax3.yaxis.tick_right()
ax3.legend(loc="lower left")
ax3.set_xlabel(r'Velocity dispersion (km/s)')
        
# Save figure
plt.savefig('plot2.pdf')
