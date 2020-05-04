# -*- coding: utf-8 -*-
# CalculadoraFunciones módulo de funciones.
from __future__ import print_function
import sympy as spp
import numpy as np
import re
import pkgutil
import matplotlib.pyplot as plt
from pylab import meshgrid,cm,imshow,contour,clabel,colorbar,axis,title,show
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from IPython.core.display import Markdown, display, clear_output, HTML
from sympy.parsing.sympy_parser import parse_expr
from sympy.solvers import solveset
from sympy.plotting import plot
from sympy.vector import cross 
from ipywidgets import interact, interactive, fixed, interact_manual, Layout
from matplotlib import style, cm
import ipywidgets as widgets

# Establece las variables globales
# Código HTML para la pestaña de instrucciones 
instructions_html = None 
data = pkgutil.get_data(__name__, "instructions.html")
instructions_html = data.decode('utf-8')

__DEBUG__ = False

# Define los nombres de las pestañas de la interfaz principal.
tab_names = ['Instrucciones', 'Mat Básicas', 'Cálculo', 'Algebra Lineal', 'Estadística', 'Cálculo Vectorial']
tab_dict = dict(enumerate(tab_names))
x = spp.Symbol('x')
y = spp.Symbol('y')


##############################################################
# Latex2Sympy
# Función que recibe una expresión en LaTex y la devuelve
# en formato Sympy.
# Autor: Carlos Alberto Trujillo
# text_in_latex: Cadena en formato LaTex
def Latex2Sympy(text_in_latex):
  try:
    #Retorna la expresión en Sympy
    return parse_latex(text_in_latex)
  except:
    if __DEBUG__:
        print(traceback.format_exc())
    else:
        print("La expresión no puede ser interpretada")
    return None

##############################################################
# GraficarFuncion
# Función que recibe función expresada en Sympy y la
# grafica.
# Autor: Karen Natalia Pulido
# funciones: Lista de funciones a graficar en formato Sympy
# style: Estilos de Grid
def GraficarFuncion(funciones, estilo):
    try:
        pt = plot(show=False)
        style.use(estilo)
        for funcion in funciones:
            p = plot(funcion, xlim=[-5,5], ylim=[-5,5], show=False)
            pt.append(p[0])
        pt[0].line_color = 'r'
        pt.show()
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("La función no se puede graficar")
    
##############################################################
# Derivar
# Función que recibe función expresada en Sympy y calcula
# su derivada en el orden establecido.
# Autor: Miguel Ángel Camargo
# funcion: Función en formato Sympy
# orden: Número entero mayor a 0 que expresa el orden de la
# derivada.
def Derivar(funcion,orden):
    try:
        df=spp.diff(funcion,x,orden)
        return df
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede derivar la función")

##############################################################
# Integrar
# Función que recibe función expresada en Sympy y calcula
# su integral con respecto a la variable establecida.
# Autor: Mateo Ruíz Mendoza
# funcion: Función en formato Sympy
# variable: Variable con respecto a la cual se integra
def Integrar(funcion,a,b,variable):
    try:
        if a==None:
            i=spp.integrate(funcion,variable)
        else:
            i=spp.integrate(funcion,(variable,a,b))
        return i
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede integrar la función")

##############################################################
# CalcularRaices
# Función que recibe función expresada en Sympy y calcula
# las raices de la función.
# Autor: Nicolle Murcia
# funcion: Función en formato Sympy
def CalcularRaices(funcion):
    try:
        s = solveset(funcion,x)
        return s
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden calcular las raices de la función")
            
##############################################################
# factorial
# Función que calcula el factoria de un número dado
# Autor: Miguel Ángel Camargo
# n: Valor para calcular el factorial
def factorial(n):
    if n <= 0:
        return 1
    else:
        return n * factorial(n - 1)
    
##############################################################
# taylor
# Función que recibe función expresada en Sympy y calcula
# la serie de Taylor.
# Autor: Miguel Ángel Camargo
# funcion: Función en formato Sympy
# x0: Punto inicial
# n: Número iteraciones
def taylor(function, x0, n):
    try:
        i = 0
        p = 0
        while i <= n:
            p = p + (function.diff(x, i).subs(x, x0)/(factorial(i)))*(x - x0)**i
            i += 1
    except:
        pass
    return p            

##############################################################
# GraficarTaylor
# Función que sirve para graficar la serie de 
# Taylor de una función.
# Autor: Miguel Ángel Camargo
# f: Función en formato Sympy
# x0: Punto inicial
# n: Número de Iteraciones
# Salto: Salto
def GraficarTaylor(f, x0 ,n, Salto, x_lims = [-5, 5], y_lims = [-5, 5], npoints = 800):
    try:
        x1 = np.linspace(x_lims[0], x_lims[1], npoints)
        display(HTML('<h3> Serie de $'+str(spp.latex(f))+'$</h3>'))
        for j in range(1, n + 1, Salto):

            func = taylor(f, x0, j)
            func= spp.sympify(func)
            y1=[func.subs(x,arr) for arr in x1]
            display(HTML('<p> Términos en la serie: ' + str(j)+'</p> <p> Expansión de Taylor: $'+spp.latex(func)+'$ '))
            plt.plot(x1, y1, label = 'Order '+ str(j))
        func_lambda = spp.lambdify(x, f, "numpy")
        plt.plot(x1, func_lambda(x1), label = 'Función de x')
        plt.xlim(x_lims)
        plt.ylim(y_lims)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.title('Aproximación de las Series de Taylor')
        plt.show()
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede graficar la serie.")        
    return

##############################################################
# InteractDerivarCalculo
# Función que maneja el interact para la operación derivar.
# Autor: Carlos Alberto Trujillo
# funcion: Función en formato Sympy
# graficar: True o False para graficar
# orden: Valor entero de 1 a 10 con el orden de la derivada
#        a calcular.
# estilo: Lista de estilos disponibles para la gráfica
# graficar: True o False para graficar
# orden: orden sobre el que se calcula la derivada
# estilo: Lista de estilos disponibles para la gráfica
def InteractDerivarCalculo(funcion, graficar, orden, estilo):
    try:
        funcion=parse_expr(funcion)
        result = Derivar(funcion, orden)
        wf = widgets.HTMLMath(
            value="$f(x)={}$ <p>".format( \
                   spp.latex(funcion)),
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        display(wf)    
        if graficar:
            funciones = [funcion, result]
            GraficarFuncion(funciones, estilo)
        strout = None
        if orden > 1:
            strout = "$\\frac{{d^{}f}}{{dx}} = {}$ <p>".format(spp.latex(orden),spp.latex(result))
        else:
            strout = "$\\frac{{df}}{{dx}} = {}$ <p>".format(spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación.")        
        

##############################################################
# InteractIntegrarCalculo
# Función que maneja el interact para la operación integrar.
# Autor: Carlos Alberto Trujillo
# funcion: Función en formato Sympy
# graficar: True o False para graficar
# variable: x o y según se quiera integrar
# limites: Tupla que representa el valor inicial y final cuando
# la integral es definida.
# estilo: Lista de estilos disponibles para la gráfica
def InteractIntegrarCalculo(funcion, graficar, variable, limites, estilo):
    try:
        funcion=parse_expr(funcion)
        variable = spp.Symbol(variable)
        a = limites[0];
        b = limites[1];
        if a==0 and b==0:
            a = None
            b = None
        result = Integrar(funcion,a,b,variable)
        wf = widgets.HTMLMath(
            value="$f(x)={}$ <p>".format( \
                   spp.latex(funcion)),
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        display(wf)    
        if graficar:
            funciones = [funcion, result]
            GraficarFuncion(funciones, estilo)
        strout = "$\\int"
        if a == None:
            strout += " f(x) = {}$ <p>".format(spp.latex(result))
        else:
            strout += "_{{{}}}^{{{}}} f(x) = {}$ <p>".format(spp.latex(a),spp.latex(b),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )               
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación.")        
        

##############################################################
# InteractCalcularRaices
# Función que maneja el interact para la operación integrar.
# Autor: Carlos Alberto Trujillo
# funcion: Función en formato Sympy
# graficar: True o False para graficar
# estilo: Lista de estilos disponibles para la gráfica
def InteractCalcularRaices(funcion, graficar, estilo):
    try:
        funcion = parse_expr(funcion)
        result = CalcularRaices(funcion)
        wf = widgets.HTMLMath(
            value="$f(x)={}$ <p>".format( \
                   spp.latex(funcion)),
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        display(wf)

        if graficar:
            funciones = [funcion]
            GraficarFuncion(funciones, estilo)
        wr = widgets.HTMLMath(
            value="Las raices son:${}$ <p>".format( \
                   spp.latex(result)),
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación.")        
                   
##############################################################
# InteractMaxMin
# Función que maneja el interact para la operación máximos
# y mínimos.
# Autor: Karen Natalia Pulido
# Modificada: Carlos Alberto Trujillo
# funcion: Función en formato Sympy
# graficar: True o False para graficar
# estilo: Lista de estilos disponibles para la gráfica
def InteractMaxMin(funcion,graficar,estilo):
    try:
        funcion = parse_expr(funcion)
        d1 = spp.diff(funcion)
        d2 = spp.diff(d1)
        wf = widgets.HTMLMath(
            value="$f(x)={}$ <br> $f'(x)={}$ <br> $f''(x)={}$".format( \
                   spp.latex(funcion),spp.latex(d1),spp.latex(d2)),
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        display(wf)
        pcriticos = spp.solve(d1, x)
        puntos = [(i,d2.subs(x,i)) for i in pcriticos]
        maximos = []
        minimos = []
        for punto in puntos:
            if punto[1].is_real and punto[1] > 0:
                maximos.append((punto[0],funcion.subs(x,punto[0])))
            elif punto[1].is_real and punto[1] < 0:
                minimos.append((punto[0],funcion.subs(x,punto[0])))
            else:
                #usar más criterios
                print("")            
        if graficar:
            funciones = [funcion]
            GraficarFuncion(funciones, estilo)
        strout = r"<div style='width: 100%;min-width: 800px;'>Se encontró(aron) {} máximo(s) <br>".format(len(maximos))
        for i in maximos:
            strout += "${}$ <br>".format(spp.latex(i))
        strout += r"Se encontró(aron) {} mínimos".format(len(minimos))
        for i in minimos:
            strout += "${}$ <br>".format(spp.latex(i))
        strout += "</div>"

        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación.")        
        
##############################################################
# InteractLims
# Función que maneja el interact para la operación límites.
# Autor: Karen Natalia Pulido
# funcion: Función en formato Sympy
# variable: Variable sobre la cual se calcula el límite
# tiende: Valor al que tiende el límite
def InteractLims(funcion,variable,tiende):
    try:
        funcion = parse_expr(funcion)
        variable = spp.Symbol(variable) 
        result = spp.limit(funcion, variable, tiende)
        strout = "$\\lim_{{{} \\to {}}} {} = {}$".format(variable,spp.latex(tiende), \
                  spp.latex(funcion),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación.")        
        
##############################################################
# InteractTaylor
# Función que maneja el interact para la Serie de Taylor
# Autor: Miguel Ángel Camargo
# funcion: Función en formato Sympy
# x0: Punto inicial
# n: Número de iteraciones
# Salto: Salto
def InteractTaylor(funcion, x0, n, Salto):
    try:
        F = parse_expr(funcion)
        return GraficarTaylor(F, x0, n, Salto)
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede obtener la serie.")

##############################################################
# InteractInversaAL
# Función que maneja el interact para la operación inversa.
# Autor: Miguel Ángel Camargo
# mat: Expresión en formato Sympy de la matriz
def InteractInversaAL(mat):
    try:
        matrix = parse_expr(mat)        
        matrix = spp.Matrix(matrix)
        result = matrix**-1
        strout = "${}^{{-1}} = {}$".format(spp.latex(matrix),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr 
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("La matriz no es invertible.")
        
##############################################################
# InteractDeterminanteAL
# Función que maneja el interact para la operación determinante.
# Autor: Miguel Ángel Camargo
# mat: Expresión en formato Sympy de la Matriz
def InteractDeterminanteAL(mat):
    try:
        matrix = parse_expr(mat)        
        matrix = spp.Matrix(matrix)
        result = matrix.det()
        strout = "$det \\left({}\\right)={}$".format(spp.latex(matrix),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede calcular el determinante de la matriz.")
            
##############################################################
# InteractMEAL
# Función que maneja el interact para la operación multiplicar
# por un escalar.
# Autor: Mateo Ruíz Mendoza
# mat: Expresión en formato Sympy de la matriz
# escalar: Valor escalar
def InteractMEAL(mat,escalar):
    try:
        matrix = parse_expr(mat)        
        matrix = spp.Matrix(matrix)
        result = escalar*matrix
        strout = "${} \\cdot {} = {}$".format(escalar, spp.latex(matrix),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede multiplicar la matriz.")
        
##############################################################
# InteractMultAL
# Función que maneja el interact para la operación multiplicar
# Autor: Mateo Ruíz Mendoza
# mat1: Expresión en formato sympy de la matriz 1
# mat2: Expresión en formato sympy de la matriz 2
def InteractMultAL(mat1,mat2):
    try:
        matrix1 = parse_expr(mat1)        
        matrix2 = parse_expr(mat2)        
        matrix1 = spp.Matrix(matrix1)
        matrix2 = spp.Matrix(matrix2)
        result = matrix1*matrix2
        strout = "${} \\cdot {} = {}$".format(spp.latex(matrix1), spp.latex(matrix2),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden multiplicar las matrices.")
                
##############################################################
# InteractCruzAL
# Función que maneja el interact para la operación producto
# cruz.
# Autor: Miguel Ángel Camargo
# mat1: Expresión en formato Sympy de la matriz 1
# mat2: Expresión en formato Sympy de la matriz 2
def InteractCruzAL(mat1,mat2):
    try:
        vector1 = parse_expr(mat1)        
        vector2 = parse_expr(mat2)        
        vector1 = spp.Matrix(vector1)
        vector2 = spp.Matrix(vector2)
        result = vector1.cross(vector2)
        op = cross(vector1,vector2)
        strout = "${} = {}$".format(spp.latex(op), spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar el producto cruz.")
                
##############################################################
# InteractSumaAL
# Función que maneja el interact para la operación suma
# Autor: Karen Natalia Pulido
# mat1: Expresión en formato Sympy de la matriz1
# mat2: Expresión en formato Sympy de la matriz2
def InteractSumaAL(mat1,mat2):
    try:
        matriz1 = parse_expr(mat1)        
        matriz2 = parse_expr(mat2)        
        matriz1 = spp.Matrix(matriz1)
        matriz2 = spp.Matrix(matriz2)
        result = matriz1+matriz2
        strout = "${} + {} = {}$".format(spp.latex(matriz1), spp.latex(matriz2), spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar la suma.")

##############################################################
# InteractTranspAL
# Función que maneja el interact para la operación transpuesta
# Autor: Miguel Angel Carvajal
# mat1: Expresión en formato Sympy de la matriz
def InteractTranspAL(mat1):
    try:
        matriz1 = parse_expr(mat1)             
        matriz1 = spp.Matrix(matriz1)
        result = matriz1.transpose()
        strout = "${}^{{T}} = {}$".format(spp.latex(matriz1),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar la operación.")
            
##############################################################
# InteractVectAL
# Función que grafica vectores en 2D
# Autor: Karen Natalia Pulido
# mat1: Lista de vectores en texto
def InteractVectAL(mat1):
    try:
        pares = ListaParesOrdenados(mat1)
        graficarVectores(pares)
        return None
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar la operación.")
            
##############################################################
# InteractRGJ
# Función que maneja el interact para la reducción Gauss-Jordan
# Autor: Karen Natalia Pulido
# mat1: Expresión en formato Sympy de la matriz
def InteractRGJ(mat1):
    try:
        matriz1 = parse_expr(mat1)             
        M = spp.Matrix(matriz1)
        M1=np.array(M.rref()[0])
        n,m=M1.shape
        N=np.zeros((n,m))
        for i in range(n):
            for j in range(m):
                N[i,j]=M1[i,j]
        N = spp.Matrix(N)
        strout = "${} = {}$".format(spp.latex(M),spp.latex(N))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar la operación.")

##############################################################
# InteractPtoPendiente
# Función que maneja el interact para la punto pendiente
# Autor: Miguel Ángel Camargo
# m: Pendiente
# b: Punto de Corte en Y
# graficar: True o False para graficar
# estilo: Lista de estilos para la gráfica
def InteractPtoPendiente(m,b,graficar,estilo):
    try:
        funcion = m*x+b
        if graficar:
            funciones = [funcion]
            GraficarFuncion(funciones, estilo)
        
        strout = "La ecuación de la recta es $f(x)={}$".format(spp.latex(funcion))
        wr = widgets.HTMLMath(
            value=strout,
    eholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar la operación.")
            
##############################################################
# InteractDosPuntos
# Función que maneja el interact para hallar la ecuación de
# la recta a partir de dos puntos.
# Autor: Carlos Alberto Trujillo
# p1: Punto1
# p2: Punto2
# graficar: True o False para graficar
# estilo: Lista de estilos para la gráfica
def InteractDosPuntos(p1,p2,graficar,estilo):
    try:
        p1 = parse_expr(p1)
        p2 = parse_expr(p2)
        m = (p2[1]-p1[1])/(p2[0]-p1[0])
        b = -m*p1[0]+p1[1]
        funcion = m*x+b
        if graficar:
            funciones = [funcion]
            GraficarFuncion(funciones, estilo)
        
        strout = "La ecuación de la recta es $f(x)={}$".format(spp.latex(funcion))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se pueden realizar la operación.")
            
##############################################################
# InteractEvalExp
# Función que maneja el interact para evaluar una expresión
# Autor: Carlos Alberto Trujillo
# funcion: Función en formato Sympy
# variable: Variable a reemplazar
# valor: Valor a reemplazar
def InteractEvalExp(funcion,variable,valor):
    try:
        funcion = parse_expr(funcion)
        variable = spp.Symbol(variable) 
        result = funcion.subs(variable, valor)
        strout = "$f({})={}$ <p> $f({})={}$".format(spp.latex(variable), spp.latex(funcion), \
               spp.latex(valor), spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede evaluar la expresión.")

##############################################################
# InteractFactorial
# Función que maneja el interact para hallar el factorial de
# un número.
# Autor: Miguel Ángel Camargo
# n: Número entero al que se le calcula el factorial
def InteractFactorial(n):
    try:
        r = factorial(n)
        strout = "El factorial de $n!={}$".format(spp.latex(r))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede calcular el factorial.")
                        
##############################################################
# InteractIneq
# Función que maneja el interact para graficar inecuaciones
# Autor: Carlos Alberto Trujillo
# funcion: inecuacion en terminos de x
# graficar: True o False para graficar la función.
# estilo: Llista de estilos para la gráfica.
def InteractIneq(funcion, graficar, estilo):
    try:
        funcion = parse_expr(funcion)
        strout = "${}$".format(spp.latex(funcion))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        if graficar:
            funciones = [funcion]
            GraficarFuncion(funciones, estilo)

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede graficar.")
            
##############################################################
# InteractExpan
# Función que maneja el interact para expandir un binomio.
# Autor: Nicolle Murcia
# funcion: Función en formato Sympy
def InteractExpan(funcion):
    try:
        funcion = parse_expr(funcion)
        result = spp.expand(funcion)
        strout = "${} = {}$".format(spp.latex(funcion),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede expandir la expresión.")

##############################################################
# Interactmcm
# Función que maneja el interact para calcular el mínimo
# común múltiplo.
# Autor: Nicolle Murcia
# num1: Número 1
# num2: Número 2
def Interactmcm(num1,num2):
    try:
        result = spp.lcm(num1,num2)
        strout = "El mínimo común múltiplo entre ${}$ y ${}$ es ${}$".format(spp.latex(num1),\
                  spp.latex(num2),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede calcular el valor.")

##############################################################
# InteractMCD
# Función que maneja el interact para calcular el máximo
# común divisor.
# Autor: Nicolle Murcia
# num1: Número 1
# num2: Número 2
def InteractMCD(num1,num2):
    try:
        result = spp.gcd(num1,num2)
        strout = "El máximo común divisor entre ${}$ y ${}$ es ${}$".format(spp.latex(num1),\
                  spp.latex(num2),spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede calcular el valor.")
            
##############################################################
# InteractDerivParc
# Función que maneja el interact para calcular las derivadas
# parciales de una función.
# Autor: Miguel Ángel Camargo
# funcion: Funcion en terminos de x y y
# df: Operación a realizar
def InteractDerivParc(funcion,df):
    try:
        f=parse_expr(funcion)
        strout = None
        if df=='{df}/{dx}':
            strout = "$\\frac{\\partial f}{\\partial x} =" 
            df1=spp.diff(f,x,1)
            strout += "{}$".format(spp.latex(df1))
        if df=='{df**2}/{dx**2}':
            strout = "$\\frac{\\partial^2 f}{\\partial x^2} ="
            df1=spp.diff(f,x,2)
            strout += "{}$".format(spp.latex(df1))
        if df=='{df}/{dy}':
            strout = "$\\frac{\\partial f}{\\partial y} ="
            df1=spp.diff(f,y,1)
            strout += "{}$".format(spp.latex(df1))
        if df=='{df**2}/{dy**2}':
            strout = "$\\frac{\\partial^2 f}{\\partial y^2} ="
            df1=spp.diff(f,y,2)
            strout += "{}$".format(spp.latex(df1))
        if df=='{df**2}/{dx*dy}':
            strout = "$\\frac{\\partial^2 f}{\\partial x\\partial y} ="
            df1=spp.diff(f,x,1)
            df2=spp.diff(df1,y,1)
            strout += "{}$".format(spp.latex(df2)) 
        if df=='{df**2}/{dy*dx}':
            strout = "$\\frac{\\partial^2 f}{\\partial y\\partial x} ="
            df1=spp.diff(f,y,1)
            df2=spp.diff(df1,x,1)
            strout += "{}$".format(spp.latex(df2))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede graficar.")
        
##############################################################
# InteractGrafica3D
# Función que maneja el interact para hallar la grafica 3D
# Autor: Karen Natalia Pulido
# funcion: Función en términos de x y y
def InteractGrafica3D(funcion):
    try:
        funcion = spp.sympify(funcion)
        Xa = np.arange(-3.0,3.0,0.1)
        Ya = np.arange(-3.0,3.0,0.1)
        X,Y = meshgrid(Xa, Ya) # grid of point
        Q = spp.lambdify([x,y], funcion, "numpy")
        Z = Q(X,Y)

        im = imshow(Z,cmap=cm.RdBu) #
        cset = contour(Z,np.arange(-1,1.5,0.2),linewidths=2,cmap=cm.Set2)
        clabel(cset,inline=True,fmt='%1.1f',fontsize=10)
        colorbar(im) 
        title('Grafica de la funcion en 3D')
        show()

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.RdBu,linewidth=0, antialiased=False)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()    
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
            
##############################################################
# InteractCoordPol
# Función que maneja el interact para graficar funciones en 
# coordenadas polares.
# Autor: Mateo Ruíz Mendoza
# r: Función en términos de t y r
def InteractCoordPol(r):
    try:
        t=spp.symbols("t")
        theta = np.arange(0,2*np.pi,0.001)
        r=spp.sympify(r)

        def cr(t,r):    
            n=len(r)
            R=[]
            T=[]
            for i in range(n):
                if r[i]>=0:
                    solr=r[i]
                    solt=t[i]
                    R.append(solr)
                    T.append(solt)
                else:
                    solr=-r[i]
                    solt=t[i]+np.pi
                    R.append(solr)
                    T.append(solt)
            return T,R 
        r=np.array([float(r.subs(t,o)) for o in theta])
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        ax.plot(cr(theta,r)[0],cr(theta,r)[1])

        plt.plot()
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
            
##############################################################
# InteractInt2Def
# Función que maneja el interact para resolver integrales  
# dobles definidas.
# Autor: Mateo Ruíz Mendoza
# r: Función en términos de x y y
# variable1: variable 1 x
# variable2: variable 2 y
# inferior: limite inferior
# superior: limite superior
# inferior_2: limite inferior interna
# superior_2: limite superior interna
def InteractInt2Def(funcion,variable1,inferior,superior,variable_2,inferior_2,superior_2):
    try:
        funcion = parse_expr(funcion)
        inferior=float(inferior)
        superior=float(superior)   
        inferior_2=float(inferior_2)
        superior_2=float(superior_2)
        T=spp.integrate(funcion,(spp.symbols(variable1),inferior,superior),(spp.symbols(variable_2),inferior_2,superior_2))
        strout = "$\\int_{{{}}}^{{{}}} \\int_{{{}}}^{{{}}} ({}) \\space d{} \\space d{} = {}$".format(spp.latex(inferior),\
                  spp.latex(superior),spp.latex(inferior_2),spp.latex(superior_2),spp.latex(funcion),\
                  spp.latex(variable1),spp.latex(variable_2),spp.latex(T))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
        
##############################################################
# InteractInt2Def
# Función que maneja el interact para resolver integrales  
# dobles definidas.
# Autor: Mateo Ruíz Mendoza
# r: Función en términos de x y y
# variable1: variable 1 x
# variable2: variable 2 y
def InteractInt2Ind(funcion,variable1,variable_2):
    try:
        funcion = parse_expr(funcion)
        T=spp.integrate(funcion,(spp.symbols (variable1)),(spp.symbols(variable_2)))
        strout = "$\\int \\int ({}) \\space d{} \\space d{} = {}$".format(spp.latex(funcion),\
                  spp.latex(variable1),spp.latex(variable_2),spp.latex(T))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")

##############################################################
# InteractInt3Def
# Función que maneja el interact para resolver integrales  
# triples definidas.
# Autor: Mateo Ruíz Mendoza
# r: Función en términos de x y y
# variable1: variable 1 x
# variable2: variable 2 y
# inferior: limite inferior
# superior: limite superior
# inferior_2: limite inferior interna
# superior_2: limite superior interna
# inferior_3: limite inferior interna
# superior_3: limite superior interna
def InteractInt3Def(funcion,variable_1, inferior,superior,variable_2,inferior_2,superior_2,variable_3,inferior_3,superior_3):
    try:
        funcion = parse_expr(funcion)
        inferior= float(inferior)
        superior=float(superior)   
        inferior_2=float(inferior_2)
        superior_2=float(superior_2)
        inferior_3=float(inferior_3)
        superior_3=float(superior_3)
        T=spp.integrate(funcion,(spp.symbols(variable_1),inferior,superior),(spp.symbols(variable_2),\
                        inferior_2,superior_2),(spp.symbols(variable_3),inferior_3,superior_3))
        strout = "$\\int_{{{}}}^{{{}}} \\int_{{{}}}^{{{}}} \\int_{{{}}}^{{{}}} ({}) \\space d{} \\space d{}\
                  \\space d{}= {}$".format(spp.latex(inferior),\
                  spp.latex(superior),spp.latex(inferior_2),spp.latex(superior_2),\
                  spp.latex(inferior_3),spp.latex(superior_3),spp.latex(funcion),\
                  spp.latex(variable_1),spp.latex(variable_2),spp.latex(variable_3),spp.latex(T))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
    
##############################################################
# InteractInt3Ind
# Función que maneja el interact para resolver integrales  
# triples indefinidass.
# Autor: Mateo Ruíz Mendoza
# r: Función en términos de x, y, z
# variable_1: variable 1 x
# variable_2: variable 2 y
# variable_3: variable 3 z
def InteractInt3Ind(funcion,variable_1,variable_2,variable_3):
    try:
        funcion = parse_expr(funcion)
        T=spp.integrate(funcion,(spp.symbols(variable_1)),(spp.symbols(variable_2)),(spp.symbols(variable_3)))
        strout = "$\\int \\int \\int ({}) \\space d{} \\space d{} \\space d{} = {}$".format(spp.latex(funcion),\
                  spp.latex(variable_1), spp.latex(variable_2), spp.latex(variable_3), spp.latex(T))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
                                        
                
def InteractLagrange(f, ecu):
    try:
        #Ingreso de la función y restricción
        f=parse_expr(f)
        r=parse_expr(ecu)
        #Calculo de sus derivadas
        dfx=f.diff(x)
        dfy=f.diff(y)
        drx=r.diff(x)
        dry=r.diff(y)
        #Definición de la ecuación a trabajar
        eq=spp.Eq(dfx*drx**-1, dfy*dry**-1)
        #Solución de sistema
        solucion = spp.solve((eq,r), (x,y))
        return solucion
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
    
##############################################################
# InteractDiagDisp
# Función que maneja el interact para graficar el diagrama
# de dispersión.
# Autor: Jorge Ali Pastran
# lista1: Lista de datos a graficar
# lista2: Lista de datos a graficar
def InteractDiagDisp (lista1,lista2):
    try:
        l1=[float(dato) for dato in lista1.split(',')]
        l2=[float(dato) for dato in lista2.split(',')]
        cr = np.corrcoef(l1,l2)
        fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        ax.set_title('Diagrama de Dispersión')
        ax.set_xlabel('Lista 1')
        ax.set_ylabel('Lista 2')    
        fig= ax.scatter(l1,l2)
        strout = "El coeficiente de correlación de los datos es ${}$".format(spp.latex(cr))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )        
        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
            
##############################################################
# InteractPromedio
# Función que maneja el interact para calcular el promedio.
# Autor: Jorge Ali Pastran
# lista1: Lista de datos 
def InteractPromedio (lista1):
    try:
        l1=[float(dato) for dato in lista1.split(',')]
        result = np.average(l1)
        strout = "El promedio de los datos es ${}$".format(spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")

##############################################################
# InteractMediana
# Función que maneja el interact para calcular la mediana.
# Autor: Jorge Ali Pastran
# lista1: Lista de datos 
def InteractMediana (lista1):
    try:
        l1=[float(dato) for dato in lista1.split(',')]
        result = np.median(l1)
        strout = "La mediana de los datos es ${}$".format(spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")

##############################################################
# InteractModa
# Función que maneja el interact para calcular la moda.
# Autor: Jorge Ali Pastran
# lista1: Lista de datos 
def InteractModa (lista1):
    try:
        l1=[float(dato) for dato in lista1.split(',')]
        counts = np.bincount(l1)
        result = np.argmax(counts)        
        strout = "La moda de los datos es ${}$".format(spp.latex(result))
        wr = widgets.HTMLMath(
            value=strout,
            placeholder='',
            description='',
            layout=Layout(width='100%'),
        )

        return wr
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
                        
##############################################################
# CalculoOperacion
# Función que recibe la operación a realizar
# Autor: Carlos Alberto Trujillo
# operación: Cadena con la operación a realizar
def CalculoOperacion(operacion):
    try:
        fn_text = widgets.Text(
                    value='sin(x)',
                    placeholder='Escriba una función',
                    description='Función:',
                    disabled=False
                )
        vr_text = widgets.Text(
                    value='x',
                    placeholder='Escriba una variable x o y',
                    description='Variable:',
                    disabled=False
                )
        gr_check = widgets.Checkbox(
                    value=False,
                    description='Graficar:',
                )
        or_int =   widgets.IntSlider(
                    value=1,
                    min=1,
                    max=10,
                    step=1,
                    description='Orden:',
                )  
        int_lim = widgets.IntRangeSlider(
                    value=[-10, 10],
                    min=-10,
                    max=10,
                    step=1,
                    description='Limites:',
                    disabled=False,
                    continuous_update=False,
                    orientation='horizontal',
                    readout=True,
                    readout_format='d',
        )        
        st_drop = widgets.Dropdown(
                   options=plt.style.available,
                   value='ggplot',
                   description='Estilo:',
                   disabled=False,
        )

        if operacion == "Integral Indefinida":
            interact(InteractIntegrarCalculo,funcion=fn_text,graficar=gr_check, \
                     variable=fixed(vr_text.value),limites=fixed((0,0)),estilo=st_drop)
        if operacion == "Integral Definida":
            interact(InteractIntegrarCalculo,funcion=fn_text,graficar=gr_check, \
                     variable=fixed(vr_text.value),limites=int_lim,estilo=st_drop)
        elif operacion == "Derivar":            
            interact(InteractDerivarCalculo,funcion=fn_text,graficar=gr_check, \
                         orden=or_int,estilo=st_drop)         
        elif operacion == "Calcular Raices":
            interact(InteractCalcularRaices,funcion=fn_text,graficar=gr_check, \
                    estilo=st_drop)
        elif operacion == "Máximos y Mínimos":
            interact(InteractMaxMin,funcion=fn_text,graficar=gr_check, \
                    estilo=st_drop)
        elif operacion == "Límites":
            fn_text.value = "1/x"
            interact(InteractLims,funcion=fn_text,variable=vr_text,tiende="oo")
        elif operacion == "Series de Taylor":
            interact(InteractTaylor, funcion=fn_text, x0= widgets.FloatText(value=1), \
                    n= widgets.IntText(value=4), Salto=widgets.IntSlider(min=1, max=3, step=1, value=1))        
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")

##############################################################
# ALOperacion
# Función que recibe la operación a realizar
# Autor: Carlos Alberto Trujillo
# operación: Cadena con la operación a realizar
def ALOperacion(operacion):
    try:
        mt1_text = widgets.Text(
                    value='[[1,0,0],[0,1,0],[0,0,1]]',
                    placeholder='Escriba una matriz',
                    description='Matriz:',
                    disabled=False
                )
        mt2_text = widgets.Text(
                    value='[[1,0,0],[0,1,0],[0,0,1]]',
                    placeholder='Escriba una matriz',
                    description='Matriz:',
                    disabled=False
                )
        es_flt =   widgets.FloatText(
                    value=1,
                    min=0,
                    max=100,
                    description='Escalar:',
                )        
        if operacion == "Inversa":
            interact(InteractInversaAL,mat=mt1_text)
        elif operacion == "Determinante":
            interact(InteractDeterminanteAL,mat=mt1_text)
        elif operacion == "Multiplicación x Escalar":
            interact(InteractMEAL,mat=mt1_text,escalar=es_flt)
        elif operacion == "Multiplicación":
            mt1_text.value = "[[1,2,3],[4,5,6]]"
            mt2_text.value = "[[7,8],[9,0],[1,2]]"            
            interact(InteractMultAL,mat1=mt1_text, mat2=mt2_text)
        elif operacion == "Transpuesta":
            interact(InteractTranspAL,mat1=mt1_text)
        elif operacion == "Suma":
            interact(InteractSumaAL,mat1=mt1_text,mat2=mt2_text)
        elif operacion == "Producto Cruz":
            mt1_text.value = "[1,2,3]"
            mt2_text.value = "[4,5,6]"
            interact(InteractCruzAL,mat1=mt1_text,mat2=mt2_text)
        elif operacion == "Vectores 2D":
            mt1_text.value = "(1,2),(2,3),(5,2)"
            interact(InteractVectAL,mat1=mt1_text)
        elif operacion == 'Reducción Gauss-Jordan':
            mt1_text.value = "[[2,-1,1,2],[3,1,-2,9],[-1,2,5,-5]]"
            interact(InteractRGJ,mat1=mt1_text)
        elif operacion == 'Independencia Lineal':
            interact(dep_or_ind,matriz="[[2,-1,1],[4,-2,2],[-1,2,5]]")
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
        
##############################################################
# MBOperacion
# Función que recibe la operación a realizar
# Autor: Carlos Alberto Trujillo
# operación: Cadena con la operación a realizar
def MBOperacion(operacion):
    try:
        fn_text = widgets.Text(
                    value='x**4 - 4*x**3 + 2*x**2 - 4*x + 1',
                    placeholder='Escriba una función',
                    description='Función:',
                    disabled=False
                )
        vr_text = widgets.Text(
                    value='x',
                    placeholder='Escriba una variable x o y',
                    description='Variable:',
                    disabled=False
                )
        vl_text = widgets.Text(
                    value='0',
                    placeholder='Escriba el valor',
                    description='Valor:',
                    disabled=False
                )
        p1_text = widgets.Text(
                    value='(2,3)',
                    placeholder='Escriba un punto',
                    description='Punto 1:',
                    disabled=False
                )
        p2_text = widgets.Text(
                    value='(3,2)',
                    placeholder='Escriba un punto',
                    description='Punto 2:',
                    disabled=False
                )
        b_flt =   widgets.FloatText(
                    value=1,
                    min=0,
                    max=100,
                    description='Corte en Y:',
                )        
        gr_check = widgets.Checkbox(
                    value=False,
                    description='Graficar:',
                )
        m_int =   widgets.IntSlider(
                    value=1,
                    min=-10,
                    max=10,
                    step=1,
                    description='Pendiente:',
                )  
        st_drop = widgets.Dropdown(
                   options=plt.style.available,
                   value='ggplot',
                   description='Estilo:',
                   disabled=False,
        )
        n_int =   widgets.IntText(
                    value=3,
                    min=0,
                    max=100,
                    description='Número:',
                )            
        n1_int =   widgets.IntText(
                    value=3,
                    min=0,
                    max=100,
                    description='Número 1:',
                )            
        n2_int =   widgets.IntText(
                    value=5,
                    min=0,
                    max=100,
                    description='Número 2:',
                )            

        if operacion == "Recta corte en Y y pendiente":
            interact(InteractPtoPendiente,m=m_int,b=b_flt,graficar=gr_check, \
                     estilo=st_drop)
        elif operacion == "Recta dados dos puntos":
            interact(InteractDosPuntos,p1=p1_text,p2=p2_text,graficar=gr_check, \
                     estilo=st_drop)
        elif operacion == "Evaluar expresión":
            interact(InteractEvalExp,funcion=fn_text,variable=vr_text,valor=vl_text)
        elif operacion == "Factorial":
            interact(InteractFactorial,n=n_int)
        elif operacion == "Inecuaciones":
            fn_text.value = "x - 3 < 0"
            interact(InteractIneq,funcion=fn_text,graficar=gr_check,estilo=st_drop)
        elif operacion == "Expansión":
            fn_text.value = "(x + 1)**5"
            fn_text.description = "Binomio:"
            interact(InteractExpan,funcion=fn_text)
        elif operacion == "mcm":
            n1_int.value = 14
            n2_int.value = 21
            interact(Interactmcm,num1=n1_int,num2=n2_int)
        elif operacion == "MCD":
            interact(InteractMCD,num1=n1_int,num2=n2_int)

    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")

##############################################################
# StatsOperacion
# Función que recibe la operación a realizar
# Autor: Carlos Alberto Trujillo
# operación: Cadena con la operación a realizar
def StatsOperacion(operacion):
    try:
        l1_text = widgets.Text(
                    value='1,2,3,4,5,6,8',
                    placeholder='Digite una lista de datos separados por coma',
                    description='Lista 1:',
                    disabled=False
                )
        l2_text = widgets.Text(
                    value='9,8,7,6,5,4,1',
                    placeholder='Digite una lista de datos separados por coma',
                    description='Lista 2:',
                    disabled=False
                )

        if operacion == "Diagrama de dispersión":
            interact(InteractDiagDisp, lista1=l1_text, lista2=l2_text)                                                     
        elif operacion == "Promedio":
            interact(InteractPromedio,lista1=l1_text)
        elif operacion == "Mediana":
            interact(InteractMediana,lista1=l1_text)
        elif operacion == "Moda":
            interact(InteractModa,lista1=l1_text)

    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
            
##############################################################
# CVOperacion
# Función que recibe la operación a realizar
# Autor: Carlos Alberto Trujillo
# operación: Cadena con la operación a realizar
def CVOperacion(operacion):
    try:
        fn_text = widgets.Text(
                    value='x**4 - 4*x**3 + 2*x**2 - 4*x + 1',
                    placeholder='Escriba una función en terminos de x y y',
                    description='Función:',
                    disabled=False
                )
        ec_text = widgets.Text(
                    value='',
                    placeholder='Escriba una función en terminos de x y y',
                    description='Restricción:',
                    disabled=False
                )
        if operacion == "Derivadas parciales":
            interact(InteractDerivParc, funcion="x**2*y+x*y**2", df=['{df}/{dx}', '{df**2}/{dx**2}',
                                                    '{df}/{dy}', '{df**2}/{dy**2}', 
                                                    '{df**2}/{dx*dy}','{df**2}/{dy*dx}'])            
        elif operacion == "Gráfica 3D":
            fn_text.value = 'x**2+2*x+3-y**2'
            interact(InteractGrafica3D,funcion=fn_text)
        elif operacion == "Coordenadas Polares":
            interact(InteractCoordPol,r="2*sin(4*t)") 
        elif operacion == "Integral Doble Indefinida":
            fn_text.value = "x**2 + y**2"
            interact(InteractInt2Ind,funcion=fn_text,variable1="x",variable_2="y")
        elif operacion == "Integral Doble Definida":
            fn_text.value = "x**2 + y**2"
            interact(InteractInt2Def,funcion=fn_text,variable1="x", inferior="1",superior="2",\
                     variable_2="y",inferior_2 ="7",superior_2="8")
        elif operacion == "Integral Triple Indefinida":
            fn_text.value = "x**2 + y**2 + z**2"
            interact(InteractInt3Ind,funcion=fn_text,variable_1="x",variable_2="y",variable_3="z")
        elif operacion == "Integral Triple Definida":
            fn_text.value = "x**2 + y**2 + z**2"
            interact(InteractInt3Def,funcion=fn_text,variable_1="x", inferior="1",superior="2",\
                     variable_2="y",inferior_2 ="7",superior_2="8", variable_3="z",inferior_3="10",\
                     superior_3="11")
        elif operacion == "Lagrange":
            fn_text.value = "x**2*y+x*y**2"
            ec_text.value = "2*y+2*x-4"
            interact(InteractLagrange,f=fn_text, ecu=ec_text)
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
                    
##############################################################
# PresentarInterfaz
# Función que construye la interfaz de usuario y la presenta
# Autor: Carlos Alberto Trujillo
def PresentarInterfaz():
    # Define las pestañas
    instructions_tab = widgets.HTMLMath(
        value=instructions_html,
        placeholder='',
        description='',
    )

    basicas_tab = widgets.Output()

    with basicas_tab:        
        dd_oper = widgets.Dropdown(
                    options=['Inecuaciones', 'Recta corte en Y y pendiente', 'Recta dados dos puntos', \
                             'Evaluar expresión', 'Factorial', 'Expansión', 'mcm', 'MCD'],
                    description='Operación:',
                  )
        interact(MBOperacion,operacion=dd_oper)

    calculo_tab = widgets.Output()

    with calculo_tab:        
        dd_oper = widgets.Dropdown(
                    options=['Derivar', 'Calcular Raices', 'Integral Indefinida', 'Integral Definida', \
                             'Máximos y Mínimos', 'Límites', 'Series de Taylor'],
                    description='Operación:',
                  )
        interact(CalculoOperacion,operacion=dd_oper)

    algebra_tab = widgets.Output()
    
    with algebra_tab:
        dd_oper = widgets.Dropdown(
                    options=['Inversa','Determinante','Suma','Multiplicación x Escalar','Multiplicación', \
                             'Transpuesta', 'Suma','Producto Cruz', 'Vectores 2D', 'Reducción Gauss-Jordan', \
                             'Independencia Lineal'],
                    description='Operación:',
                  )
        interact(ALOperacion,operacion=dd_oper)
    
    stats_tab = widgets.Output()
    
    with stats_tab:
        dd_oper = widgets.Dropdown(
                    options=['Diagrama de dispersión','Promedio','Mediana', 'Moda'],
                    description='Operación:',
                  )
        interact(StatsOperacion,operacion=dd_oper)

    cvect_tab = widgets.Output()
    
    with cvect_tab:
        dd_oper = widgets.Dropdown(
                    options=['Derivadas parciales','Gráfica 3D', 'Coordenadas Polares', 'Integral Doble Indefinida', \
                             'Integral Doble Definida', 'Integral Triple Indefinida', 'Integral Triple Definida', \
                             'Lagrange'],
                    description='Operación:',
                  )
        interact(CVOperacion,operacion=dd_oper)    

    interface_tabs = widgets.Tab(
        children=[instructions_tab,basicas_tab,calculo_tab,algebra_tab, stats_tab, cvect_tab], _titles=tab_dict)

    return interface_tabs

def reduccion(matriz):
    try:
        matriz=spp.sympify(matriz)
        M=spp.Matrix(matriz)
        M1=np.array(M.rref()[0])
        n,m=M1.shape
        N=np.zeros((n,m))
        for i in range(n):
            for j in range(m):
                 N[i,j]=M1[i,j]
        return N
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")        
  
def dep_or_ind(matriz):
    try:
        M=reduccion(matriz)
        n,m=M.shape
        for i in range(n):
            k=0
            for j in range(m):
                if M[i,j]==0:
                    k=k+1
                    if k==m:
                      text="Son linealmente dependientes"
                    else:
                      text="Son linealmente independientes"
        return text
    except:
        if __DEBUG__:
            print(traceback.format_exc())
        else:
            print("No se puede realizar la operación")
            
##############################################################
# Clase ParOrdenado
# Objeto para almacenar pares ordenados
# Autor: Karen Natalia Pulido
class ParOrdenado:
    def __init__(self,a,b):
        self.real = float(a)
        self.imaginario = float(b)

##############################################################
# graficarVectores
# Funcion que grafica vectores
# Autor: Karen Natalia Pulido
# lista: lista de pares ordenados
def graficarVectores(lista):
    x = [0]*len(lista)
    y = [0]*len(lista)
    u = []
    v = []
    for vector in lista:
        u.append(vector.real)
        v.append(vector.imaginario)
    izq = min(-1, min(u)-1)
    der = max(1, max(u)+1)
    abajo = min(-1, min(v)-1)
    arriba = max(1, max(v)+1)
    plt.quiver(x, y, u, v,  angles='xy', scale_units='xy', scale=1)
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')
    plt.xlim([izq, der])
    plt.ylim([abajo, arriba])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.gca().set_title("Graficación de vectores")
    plt.show()
    return plt.gca()

##############################################################
# ListaParesOrdenados
# Funcion que convierte una cadena de texto en formato 
# "(a,b),(c,d),...(x,y)" a una lista de pares ordenados
# Autor: Karen Natalia Pulido
# lista: texto con lista de pares ordenados
def ListaParesOrdenados(vector_raw_text):
    pares = []
    cifras = list(map(float, re.findall(r"\d+(?:\.\d+)?", vector_raw_text)))
    lista = np.reshape(cifras,(-1,2))
    for par in lista:
        pares.append(ParOrdenado(par[0],par[1]))
    return pares
			