import datetime, glob, re, sys, time, os, copy, logging
from pygments import highlight
from pygments.lexers import BashLexer, PythonLexer
from pygments.formatters import HtmlFormatter

def convert(cellList):
    # Return a deep copy of cellList with code replaced with html-ized code
    tempCells=copy.deepcopy(cellList)
    for cell in tempCells:
        cell['source'] = \
                [highlight(source, PythonLexer(), HtmlFormatter()) \
                for source in cell['source']] 

        for output in cell['outputs']:
            if output['output_type'] == 'execute_result':
                output['data']['text/plain'] = \
                        [highlight(text, BashLexer(), HtmlFormatter()) \
                        for text in output['data']['text/plain']]

            if output['output_type'] == 'error':
                output['traceback'] = \
                        [highlight(text, BashLexer(), HtmlFormatter()) \
                        for text in output['traceback']]
    return tempCells 

def output(output):
    temp_output=copy.deepcopy(output)
    for cell in temp_output:
        if cell:
            if cell['image/png']:
                cell['image/png']='<img src="data:image/png;base64, '+cell['image/png']+'" />'
            if cell['stdout']:
                cell['stdout']=highlight(cell['stdout'], BashLexer(), HtmlFormatter())
            if cell['stderr']:
                cell['stderr']=highlight(cell['stderr'], BashLexer(), HtmlFormatter())
    return temp_output

