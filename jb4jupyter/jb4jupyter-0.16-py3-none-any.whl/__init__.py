from .plotpretty import *
import os
from IPython.display import display, Latex
import itertools
from scipy.optimize import fsolve
import warnings
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.notebook_repr_html', True)
# this is some craziness https://stackoverflow.com/questions/20685635/pandas-dataframe-as-latex-or-html-table-nbconvert
pd.set_option('display.notebook_repr_html', True)
def _repr_latex_(self):
    return "\\begin{center}{%s}\end{center}" % self.to_latex(escape=False)
pd.DataFrame._repr_latex_ = _repr_latex_  # monkey patch pandas DataFrame
pd.DataFrame._repr_latex_ = _repr_latex_

from IPython.display import display, HTML

CSS = """
#notebook-container{
    background-color: #111;
}
.body{
    background-color: #111;
}
.text_cell.rendered .rendered_html{
    color: white;
}
div.output_subarea{
    max-width: 65vw;
    padding-left: 10vw;
}
div.output_area .rendered_html table {
  margin-left: 10vw;
  margin-right: 0;
}
"""
def html_dark():
	HTML('<style>{}</style>'.format(CSS))
	DONOTHING=0

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
