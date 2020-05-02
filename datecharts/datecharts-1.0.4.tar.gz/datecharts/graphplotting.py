'''
Created on 19. 4. 2020

@author: ppavlu
'''

import matplotlib.pyplot as plt
from matplotlib import interactive
#from matplotlib.dates import drange
import numpy as np
import datetime

interactive(False)

MONTHMAP={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,
          'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
UNAVAIL=None #representation of missing value

def DemoGraph():
    x = np.linspace(0.1, 2 * np.pi, 41)
    y = np.exp(np.sin(x))

    plt.stem(x, y, use_line_collection=True)
    plt.show()

def DemoDiscreteGraph():
    x=[1,2,3,4,5,6,7,8,9,10]
    y=[2.3,2.5,2.7,2.8,2.85,2.8,2.6,2.3,2.0,1.8]
    #plt.stem(x,y, use_line_collection=True)
    #plt.show()
    #plt.ion()
    plt.plot(x,y)
    #vstup=input("Press any key to continue...")
    #plt.draw()
    #clear_output(wait=True)
    #time.sleep(10)
    plt.show()
    #time.sleep(10)
    #clear_output(wait=True)
    #plt.show()
    
    
    
def PlotTimeSeries(x,y): 
    #simple drawing of series of data
    plt.stem(x,y, use_line_collection=True)
    plt.show()
    
def ConvertStringValues(values,placeholder,miss): 
    #list of string value representations, converts to values (int or float)
    #missing values (miss) represented by placeholder value
    dataset=[]
    for s in values:
        if (s == miss):
            dataset.append(placeholder)
        elif s.isalnum():
            dataset.append(int(s))
        else:
            dataset.append(float(s))
    return dataset

def ConvertStringDateTime(line):
    #converts text with date/time moment to a dict of values
    #structure expected: "Wed Apr 22 18:07:54 2020"
    NUMELEMENTS=5 #number of elements in the text format of the timestamp
    
    if (line == ""):
        stamp=None
    else:
        if ("" in line.split(sep=" ")):
            vals=[]
            for t in line.split(" "):
                if (t != ""):
                    vals.append(t)
        else:
            vals=line.split(sep=" ")
        if len(vals) != NUMELEMENTS:
            stamp=None
        else:
            stamp={'year':int(vals[NUMELEMENTS-1])}
            stamp.update({'month':MONTHMAP[vals[NUMELEMENTS-4]]})
            stamp.update({'day':int(vals[NUMELEMENTS-3])})
            stamp.update({'hour':int(vals[NUMELEMENTS-2][0:2])})
            stamp.update({'minute':int(vals[NUMELEMENTS-2][3:5])})
            stamp.update({'Second':int(vals[NUMELEMENTS-2][6:8])})
    return stamp

def ConvertDTValues(dtlist):
    #converts the series of date/time points from text format to matplotlib format
    #structure expected is set of strings like "Wed Apr 22 18:07:54 2020", converts to 
    #a set of converted values
    dtset=[]
    for line in dtlist:
        dtdict=ConvertStringDateTime(line)
        dt=datetime.datetime(dtdict['year'],dtdict['month'],dtdict['day'],dtdict['hour'],dtdict['minute'])
        dtset.append(dt)
    return dtset    

def PlotValuesInTime(datetimes,values,miss,valtext): 
    #plot series, input as two string lists, valtype is text for title
    yvals=ConvertStringValues(values, UNAVAIL, miss) #convert set of strings to values
    #preparing the range of x=axis - dates and times
    
    #startTime=ConvertStringDateTime(datetimes[0])
    #endTime=ConvertStringDateTime(datetimes[len(datetimes)-1])
    #startTimePoint=datetime.datetime(startTime['year'],startTime['month'],startTime['day'],startTime['hour'],startTime['minute'])
    #endTimePoint=datetime.datetime(endTime['year'],endTime['month'],endTime['day'],endTime['hour'],endTime['minute'])
    #timePointsDelta=datetime.timedelta(minutes=10)
    #xdates=drange(startTimePoint,endTimePoint,timePointsDelta)
    xdates=ConvertDTValues(datetimes)
    
    fig, ax = plt.subplots() #creating chart structuresd
    
    ax.plot_date(xdates,yvals,fmt='o-') 
    ax.set_title(valtext)
    fig.autofmt_xdate()
    
    plt.show()

if __name__ == '__main__':
    pass