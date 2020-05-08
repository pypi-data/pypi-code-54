from itertools import zip_longest
from multiprocessing import Process
import time, sys, datetime, glob, re, sys, time, os, copy, logging, threading, queue
from hashlib import md5
from io import StringIO
from subprocess import Popen, PIPE
from flask import url_for
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import thebe.core.constants as Constant
import thebe.core.output as output 
import thebe.core.logger as Logger
import thebe.core.update as Update
#from thebe.core.output import outputController 
logger = Logger.getLogger('run.log', __name__)

def runNewCells(socketio, cellsToRun, globalScope, localScope):
    '''
    Run each changed cell, returning the output.
    '''

    cellOutput = []
    for cellCount, cell in enumerate(cellsToRun):
        #Keep the master list updated
        if cell['changed']:
            socketio.emit('message', 'Running cell #%s'%(cellCount))
            socketio.emit('loading', cellCount)
            logger.info('\n------------------------\nRunning cell #%s\n-------------------------------\
                    \nWith code:\n%s'%(cellCount, cell['source']))
            stdout, stderr, plotData = runWithExec(socketio, cell['source'], globalScope, localScope)

            clearOutputs(cell)

            fillPlot(cell, plotData)
            fillStdOut(cell, stdout)
            fillErr(cell, stderr)

            # How does ipython do this?
            cell['changed']=False
            cell['execution_count'] = cell['execution_count'] + 1
            logger.info('exe co: %s'%(cell['execution_count'],))

#            logger.debug('Cell source, in output class:\t%s\n'%(cell['source']))

        cellOutput.append(cell)

    return cellOutput

def runWithExec(socketio, cellCode, globalScope, localScope):
    '''
    runs one cell of code and return plotdata and std out/err
    '''

    #Append the current working directory to path(not sure if this is necessary)
    sys.path.append(os.getcwd())

#    oldGlobalScope = copy.deepcopy(globalScope)
#    oldLocalScope = copy.deepcopy(localScope)
    
    #Save the old output location
    oldstdout = sys.stdout

    #Redirect system output, and initialize system error
    stdout = sys.stdout=StringIO()
    stderr = ''
    plotData = ''

    #Set cutoff var for output
    isRunning = queue.Queue()
    isRunning.put(True)
    #Create a thread to stream the output to the client during runtime.
    t = threading.Thread(target = Update.streamOutput, \
            args = (socketio, stdout, isRunning))  
    t.daemon = True
    t.start()

    #Run code and capture output, if there is an error stop running, and capture it.
    try:
        exec(''.join(cellCode), globalScope, localScope)
        sys.stdout = oldstdout
        stdout = stdout.getvalue() 
        sys.path.pop()
        plotData = getPlotData(globalScope, localScope)

    except Exception as e:
#        globalScope = oldGlobalScope
#        localScope = oldLocalScope
        stderr = str(e)
        sys.stdout = oldstdout
        stdout = stdout.getvalue() 
        sys.path.pop()

    #Turn off streamOutput
    isRunning.put(False)

    return stdout, stderr, plotData

def getPlotData(globalScope, localScope):
    '''
    '''

    code=Constant.GetPlot
    redirected_output=sys.stdout=StringIO()
    redirected_error=sys.stderr=StringIO()
    stdout=''
    stderr=''
    sys.path.append(os.getcwd())
    try:
        exec(code, globalScope, localScope)
        stdout=redirected_output.getvalue().rstrip()
        stderr=''
    except Exception as e:
        stdout=redirected_output.getvalue()
        stderr=str(e)
    sys.path.pop()
    sys.stdout=sys.__stdout__
    sys.stderr=sys.__stderr__
    if stdout==Constant.EmptyGraph:
        stdout=''
    return stdout

def clearOutputs(cell):
    '''
    Replace list of outputs with an empty one.
    '''
    cell['outputs'] = []

def fillPlot(cell, plot):
    '''
    If an image exists in the plot variable, create and return a plot cell.
    '''
    if plot:
        output = Constant.getDisplayOutput()
        output['data']['image/png'] = plot
        cell['outputs'].append(output)

def fillStdOut(cell, stdOut):
    '''
    If an output exists in the stdOut variable append new output to cell reference.
    '''
    if stdOut:
        output = Constant.getExecuteOutput()
        output['data']['text/plain'] = stdOut.splitlines(True)
        cell['outputs'].append(output)

def fillErr(cell, err):
    '''
    If an output exists in the err variable, create and return a err cell.
    '''
    if err:
        output = Constant.getErrorOutput()
        output['traceback'] = err.splitlines(True)
        cell['outputs'].append(output)

