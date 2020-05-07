from .plotpretty import *
import os
import itertools
from IPython.display import display, Latex
import warnings

warnings.filterwarnings('ignore')

def latexdisplay(varname,varval,roundto=3):
    return display(Latex('$' + varname + '= $' + str(round(varval,roundto))))

def latexdisplayunits(varname,varval,units,roundto=3):
    return display(Latex('$' + varname + '= $' + str(round(varval,roundto)) + ' $' + units + '$'))

def variablename(var):
    import itertools
    return str(([tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())])[0])

def brint(var,units='',roundto=3):
    if units == '':
        if var == str(var):
            return display(Latex(var))
        else:
            return latexdisplay(variablename(var),var,roundto)
    else:
        return latexdisplayunits(variablename(var),var,units,roundto)


def joke(): return 'nah'

def exporthtml():
	os.system('jupyter nbconvert --to=html ' +  os.path.abspath(__file__))

def exportpdf():
	os.system('jupyter nbconvert --to=pdf --template=jb4jupyter ' + os.path.abspath(__file__))

def configlatexprint():
	lines = [
		'((* extends \'article.tplx\' *)) \n',
		'((* block input_group *)) \n',
		'((* endblock input_group *)) \n',
		'((* block execute_result scoped *)) \n',
		'    ((* block display_data scoped *)) \n',
		'        ((( super() ))) \n',
		'    ((* endblock display_data *)) \n',
		'((* endblock execute_result *)) \n'
		]
	with open('jb4jupyter.tplx','w') as txtfile:
		txtfile.writelines(lines)
