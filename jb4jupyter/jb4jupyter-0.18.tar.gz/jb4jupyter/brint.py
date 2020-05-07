from IPython.display import display, Latex

def latexdisplay(varname,varval,roundto=3):
    return display(Latex('$' + varname + '= $' + str(round(varval,roundto))))

def latexdisplayunits(varname,varval,units,roundto=3):
    return display(Latex('$' + varname + '= $' + str(round(varval,roundto)) + ' $' + units + '$'))

def variablename(var):
    # import itertools
    # return str(([tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())])[0])
    return str([tpl[0] for tpl in filter(lambda x: var is x[1], globals().items())][0])

def brint(var,units='',roundto=3):
    if units == '':
        if var == str(var):
            return display(Latex(var))
        else:
            return latexdisplay(variablename(var),var,roundto)
    else:
        return latexdisplayunits(variablename(var),var,units,roundto)
