# -*-coding:utf-8-*-
# Read vtk data generated from the command of `foamToVTK`

import numpy as np
import matplotlib.pyplot as plt
import sciPyFoam.readvtk as readvtk
import sciPyFoam.figure as scifig

def readPatch(caseDir, patch, time, fieldName,name_fmt=lambda  patch,time : str('%s_%s.vtk'% (patch,time)),coord2km=False, depthPositive=False, K2C=True, eval_patchIndex=None):
    
    fname=caseDir+'/VTK/'+patch+'/'+name_fmt(patch,time)
    triangles,field=readvtk.readPolyData(fname,fieldName,coord2km, depthPositive, K2C, eval_patchIndex)
    return triangles,field

def readPatchMesh(caseDir, patch, time,name_fmt=lambda  patch, time : str('%s_%s.vtk'% (patch,time)),coord2km=False, depthPositive=False, eval_patchIndex=None):
    
    fname=caseDir+'/VTK/'+patch+'/'+name_fmt(patch,time)
    x,y, z,edges=readvtk.readPolyMesh(fname,coord2km, depthPositive, eval_patchIndex)
    
    return x,y, z, edges