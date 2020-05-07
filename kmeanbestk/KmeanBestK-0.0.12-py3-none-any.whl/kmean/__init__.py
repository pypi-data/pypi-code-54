
import numpy
import os

# load dataset
def loadDataSet(inputFile):
    inputData= open(inputFile,'r')
    result=list()
    for line in inputData.readlines():
        col = line.split()
        numList= list()
        for item in col:
            numList.append(item)            
        result.append(numList)
    return result

def initCentroids(dataset, k):
    index_1=numpy.random.choice(len(dataset),k)
    initdata= list()
    for i in range (len(index_1)):
        initdata.append(dataset[index_1[i]])
    return initdata

def calculateDis(vector1, vector2):
    vector1=vector1.astype(numpy.float)
    vector2=vector2.astype(numpy.float)

    return numpy.sqrt(numpy.sum(numpy.square(vector1 - vector2)))

def getClusters(dataSet, centroidsData, k):
    cluster= dict()
    for item in dataSet:
        vector1 = numpy.array(item)
        minDis = float("inf")
        flag =0
        
        for i in range (0,k):
            if i not in cluster.keys():
                cluster[i]=list()
            vector2 = numpy.array(centroidsData[i])
            distance = calculateDis(vector1, vector2)
            
            if distance < minDis:
                minDis= distance
                flag=i
        cluster[flag].append(item)
    return cluster

def getVariance(cluster,centroidsData):
    sum =0.0
    for key in cluster.keys():
        vector1= numpy.array(centroidsData[key])
        distance=0.0
        for item in cluster[key]:
            vector2= numpy.array(item)
            distance+=calculateDis(vector1, vector2)
        sum+=distance
    return sum


def getCentroids(cluster):
    newCentroidList= list()
    for key in cluster.keys():
        line= numpy.array(cluster[key])
        line = line.astype(numpy.float)
        centroid = numpy.mean(line,axis=0)  
        newCentroidList.append(centroid)
    return numpy.array(newCentroidList).tolist()
    
    
def getSSE(cluster,centroidsData):
    sum =0.0
    for key in cluster.keys():
        vector1= numpy.array(centroidsData[key])
        distance=0.0
        for item in cluster[key]:
            vector2= numpy.array(item)
            distance+=calculateDis(vector1, vector2)
        sum+=distance
    return sum

def Silhouette(cluster):
    count =0
    sumSi = 0.0
    for key in cluster.keys():
        count+=len(cluster[key])
        for item in cluster[key]:
            disAi = 0.0
#             disBi = 0.0
            ai = 0.0
            bi = float("inf")
            si = 0.0
            # countBi = 0
            vector1= numpy.array(item)
            
            #calculate each ai
            if len(cluster[key])>1:
                for item2 in cluster[key]:
                    vector2 = numpy.array(item2)
                    disAi += calculateDis(vector1,vector2)
                ai = disAi/(len(cluster[key])-1)

                # calculate each bi
                for key2 in cluster.keys():
                    if key2!=key:
                        disBi = 0.0
                        countBi=len(cluster[key2])
                        if countBi>0:
                            for item3 in cluster[key2]:
                                vector3 = numpy.array(item3)
                                disBi +=  calculateDis(vector1,vector3)
                            bi = min(bi, disBi/countBi)
                # calculate si
                if max(bi,ai)!=0.0:
                	si= (bi-ai)/(max(bi,ai))
            elif len(cluster[key])==1:
            	si=0.0
            sumSi+=si
    if count!=0:
    	return sumSi/count
    else:
    	return 0.0

def kmean(kclass,result,inFile):          
    dataSet = loadDataSet(inFile)                     
    centroidList = initCentroids(dataSet, kclass)
    clusterDict = getClusters(dataSet, centroidList,kclass) 
    newVar = getVariance(clusterDict, centroidList)        
    oldVar = 1                                 
 
    time = 2
    while abs(newVar - oldVar) >= 0.00001 and time <300:                     
        centroidList = getCentroids(clusterDict)  
        clusterDict = getClusters(dataSet, centroidList,kclass)  
        oldVar = newVar                                   
        newVar = getVariance(clusterDict, centroidList)
        time += 1
    si=Silhouette(clusterDict)
    result.append(si)


def bestK():

    print("please input the inputfile path: ")
    inFile= input()
    if os.path.exists(inFile)==False:
        print("file not exist")
        return 
    inFileName=os.path.split(inFile)
    print(inFileName[1])
    result=[]

    print("please input the maximun class number: ")
    maxK =input()
    maxK= int(maxK)
    for i in range(2,maxK):
        kmean(i,result,inFile)
    print(result.index(max(result))+2)
    outFile = open("outkmean.txt",'a+')
    outFile.write(inFileName[1]+ ": " + str(result.index(max(result))+2)+"\n" )
    return 
    
