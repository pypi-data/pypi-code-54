from itertools import zip_longest
import time, sys, datetime, glob, re, sys, time, os, copy, logging
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import thebe.core.constants as Constants
def update(oldCellList, fileContent, runAll=False):
    '''
    Determine which cell has changed, since the file has changed.
    Return a list of cells, with updated sources, and the changed
    variable set.
    '''

    cellList = []
    sourceList = getSourceList(oldCellList)

    for cellCount, source in enumerate(list(filter(None, fileContent.split(Constants.CellDelimiter)))):
        #Hash to be used for identifying priviously run code
#        cellSource=hashCode(source)
        #Split source filed by line
        source = source.splitlines(True)

        #Set outputs
        cell = setOutputs(oldCellList, source, sourceList)

        #Set Code
        cell['source'] = source

        cell['outputs'] = [Constants.getExecuteOutput()]

        if runAll:
            cell['changed']=True

        #Set execution counter
        try:
            cell['execution_count'] = oldCellList[cellCount]['execution_count'] 
        except IndexError:
            pass

        cellList.append(cell)

    return cellList

def getSourceList(cellList):
    '''
    Form the hashes from the cell list into a list
    '''
    return [cell['source'] for cell in cellList]

def toThebe(ipynb):
    '''
    Take in a ipynb dictionary, and returns a string in thebe format.
    (Cell sources to delimited by our Constants.CellDelimiter)
    '''

    return Constants.CellDelimiter.join([''.join(cell['source']) for cell in ipynb['cells']])
    

def setOutputs(oldCellList, cellSource, sourceList):
    '''
    Set outputs of cell depending on whether it has been run before 
    '''
    return assembleCell(oldCellList, sourceList, cellSource)

def assembleCell(oldCellList, sourceList, cellSource):
    '''
    If the source preexists, set new cell to old cell
    If not, set changed, and last changed time.
    '''

    cell=copy.deepcopy(Constants.Cell)

    try:
        x=sourceList.index(cellSource)
        cell=oldCellList[x]

    except ValueError:
        cell['execution_count']
        cell['changed']=True
        cell['last_changed']=time.strftime("%x %X", time.gmtime())

    return cell

#Hash the string of code
def hashSource(source):
    return md5(source.encode()).hexdigest()
