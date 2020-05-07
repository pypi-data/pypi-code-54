from .plotpretty import *
from .brint import *
import os
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
