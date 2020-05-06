import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, interact_manual, widgets
import numpy as np
import sympy as spp
from sympy.parsing.sympy_parser import parse_expr
from mpl_toolkits.mplot3d import Axes3D
from sympy.plotting import plot3d,plot
from IPython.display import display, Markdown

x,y,z,w = spp.symbols('x y z w')

def pre_algebra(Tema, Funcion) :
    try:                                     
        if Tema == 'Operaciones Básicas':
            print(float(parse_expr(Funcion)))
            
        if Tema == 'Factores y Números primos' :
            Funcion = int(Funcion)
            def fn(segundo_valor,máximo_común_divisor, Numero_primo):
                if máximo_común_divisor == True:
                    def mcd(Funcion, segundo_valor):
                        segundo_valor= parse_expr(segundo_valor)
                        Funcion, segundo_valor=max(int(Funcion), segundo_valor),min(int(Funcion), segundo_valor)
                        while segundo_valor!=0: 
                            Funcion, segundo_valor=segundo_valor,Funcion%segundo_valor 
                        return Funcion    
                    print(mcd(int(Funcion), segundo_valor))
                if Numero_primo == True:
                    def pri(Funcion):
                        phi=0
                        for i in range(1,Funcion):
                            ai=Funcion 
                            while i!=0:
                                ai,i=i,ai%i
                            if ai==1:
                                phi+=1
                        if phi== Funcion-1:
                            print("El numero", Funcion, "es primo.")
                        elif phi < Funcion-1:
                            print("El numero", Funcion, " no es primo.")
                    print(pri(Funcion))
            interact(fn, segundo_valor='', máximo_común_divisor= False, Numero_primo= False)

        if Tema == 'Logaritmos, Radicales y Exponenciales' :                          # Tema: Logaritmos, Radicales y Exponenciales
            def l(n, Logaritmos, Logaritmos_Naturales, Radicales, Exponenciales) :
                n = parse_expr(n)
                if Logaritmos == True: 
                    try:                                                         # Logaritmos
                        huk = np.log(int(Funcion))/np.log(int(n))
                        print(huk)
                    except:
                        pass
                if Logaritmos_Naturales == True :
                    try:
                        print(np.log(int(Funcion)))
                    except:
                        pass
                if Radicales == True:                                         # Radicales
                    try:                                                          
                        n2=(int(Funcion))**(1/n)
                        print(spp.N(n2))
                    except:
                        pass
                if Exponenciales == True:                                     #Exponenciales
                    try:
                        n3=(int(Funcion))**n
                        print(n3)
                    except:
                        pass
            interact(l, n='',  Logaritmos = False, Logaritmos_Naturales = False, Radicales = False, Exponenciales = False)
    except:
        pass

def algebra_lineal(Tema):   
    def ing_matrizU(matriz):
        try:
            matriz=parse_expr(matriz)
            m = spp.Matrix(matriz)
            global U
            U = m
            return 
        except: 
            print("Al parecer escribiste mal la matriz")

    def ing_matrizV(matriz):
        try:
            matriz=parse_expr(matriz)
            m = spp.Matrix(matriz)
            global V 
            V = m
            return
        except: 
            print("Al parecer escribiste mal la matriz")
        
    mat1=widgets.Text(description="Matriz",value="[[1,0],[0,1]]")
    mat2=widgets.Text(description="Matriz",value="[[1,0],[0,1]]")
    
    if Tema == 'Operaciones entre matrices':
        def sumar(n,m):
            try:
                print("Ingrese 2 matrices de igual tamaño para ser sumadas")
                suma=n+m
                return suma
            except: 
                print("Las matrices no pueden ser sumadas")
        def resta(s,j):
            try:
                print("Ingrese 2 matrices de igual tamaño para ser restadas")
                restar=s-j
                return restar
            except: 
                print("Las matrices no pueden ser restadas")
        def multi(n,m):
            try:
                print("Ingrese 2 matrices: La primera de tamaño m*n y la segunda n*p para ser multiplicadas")
                multi_vec=n*m
                return multi_vec
            except:
                print("No se puede realizar la multiplicacion entre matrices")
        def invert(m):
            try:
                matri_inv=m**-1
                return matri_inv
            except:
                print("Error:La inversa de una matriz solo puede ser calculada para matrices cuadradas")
        def det(m):
            try:
                dt=m.det()
                return dt
            except:
                print("Esta matriz no tiene determinante ya que debe ser cuadrada")


        def f(Operacion,m1,m2):
            mat1=ing_matrizU(m1)
            mat2=ing_matrizV(m2)
            m = U
            r = V
            if Operacion == 'Suma':
                k=sumar(m,r)
                k
            if Operacion == 'Resta':
                k=resta(m,r)
                k
            if Operacion == 'Multiplicación':
                k=multi(m,r)
                k
            if Operacion == 'Inversa':
                k=invert(m)
                l=invert(r)
                def inv(Inversa_1,Inversa_2):
                    if Inversa_1 == True:
                        print("Matriz inversa de la primera matriz",k)
                    if Inversa_2 == True:
                        print("Matriz inversa de la segunda matriz",l)
                    return inv
                interact(inv, Matriz='',  Inversa_1 = False, Inversa_2 = False)
                
            if Operacion == 'Determinante':
                k=det(m)
                l=det(r)
                def DET(Determinante_1,Determinante_2):
                    if Determinante_1 == True:
                        print("El determinante de la primera matriz es ",k)
                    if Determinante_2 == True:
                        print("El determinante de la segunda matriz es ",l)
                    return DET
                interact(DET, Matriz='',  Determinante_1= False, Determinante_2 = False)
            return k
        interact(f, Operacion =['Suma','Resta','Multiplicación','Inversa','Determinante'],m1=mat1,m2=mat2)
    
    if Tema == 'Sistema de ecuaciones lineales':
        def solucion(n,m):
            try:
                solucion1=spp.linsolve((n,m),[x,y,z])
                return solucion1
            except: 
                print("Ups ocurrio algo, revisa la matriz")
        def g(tema,m1,m2):
            mat1=ing_matrizU(m1)
            mat2=ing_matrizV(m2)
            m = U
            r = V
            if tema == 'Solución por eliminación':
                print("Ingrese las matrices: Tenga en cuenta que la primera matriz es la matriz aumentada y la segunda es el resultado de la matriz aumentada")
                k=solucion(m,r)
                k
            return k
        interact(g, tema ='Solución por eliminación',m1=mat1,m2=mat2)
    if Tema == 'Operaciones entre vectores':
        import numpy as np            
        def ing_matrizV(vector):
            try:
                vector=parse_expr(vector)
                vec_1= np.array(vector)
                m=vec_1[np.newaxis, :]
                global V 
                V = m
                return
            except: 
                print("Al parecer escribiste mal el vector")
        def ing_matrizU(vector):
            try:
                print("Ingresa dos vectores, recuerda que debe ser entre paréntesis y separado por comas: (1,2)")
                vector=parse_expr(vector)
                vec_1= np.array(vector)
                m=vec_1[np.newaxis, :]            
                global U
                U = m
            except: 
                print("Al parecer escribiste mal el vector")
        mat3=widgets.Text(description="Vector",value="(1,0)")
        mat4=widgets.Text(description="Vector",value="(1,0)")
        def sumar2(n,m):
            try:
                suma2=n+m
                return suma2
            except: 
                print("Los vectores no pueden ser sumados")
        def resta2(s,j):
            try:
                restar2=j+-s
                return restar2
            except: 
                print("Los vectores no pueden ser restados")  
        def h(tema,m1,m2):
            mat3=ing_matrizU(m1)
            mat4=ing_matrizV(m2)
            m = U
            r = V
            if tema == 'Suma entre vectores':
                k=sumar2(r,m)
                print("Este es el resultado de sumar dos vectores:",k)
            if tema == 'Resta entre vectores':
                k=resta2(r,m)
                k
                return k
            if tema == 'Multiplicación':
                def ing_matrizZ(vector):
                    try:
                        vector=parse_expr(vector)
                        vec_1= np.array(vector)
                        m=vec_1[np.newaxis, :]
                        global V 
                        V = m
                    except: 
                        print("Al parecer escribiste mal el vector")
                def ing_matrizW(vector):
                    try:
                        print("Ingresa un vector y un escalar, recuerda que el vector debe ser entre paréntesis y separado por comas: (1,2)")
                        vector=parse_expr(vector)
                        m=vector           
                        global U
                        U = m
                    except: 
                        print("Al parecer escribiste mal el escalar")
                mat3=widgets.Text(description="Vector",value="(1,0)")
                mat4=widgets.Text(description="Escalar",value="#")
                def multip(n,m):
                    try:
                        multi_vec=n*m
                        return multi_vec
                    except:
                        print("No se puede realizar la multiplicacion por escalar")
                def i(tema,m1,m2):
                    mat3=ing_matrizZ(m1)
                    mat4=ing_matrizW(m2)
                    m = U
                    r = V
                    if tema == 'Multiplicación por escalar':
                        P=multip(m,r)
                        P
                    return P
                interact(i,tema='Multiplicación por escalar',m1=mat3,m2=mat4)
                
        interact(h, tema =['Suma entre vectores','Resta entre vectores','Multiplicación'],m1=mat3,m2=mat4)
    
    
    
def calculo_diferencial(Tema, Funcion):
    button1, button2 = widgets.Button(description="Dos Dimensiones"), widgets.Button(description="Tres Dimensiones")
    output1, output2 = widgets.Output(), widgets.Output()
    display(button1,output1); display(button2,output2)
    def DosD(dosd) :                            # 2D
        with output1:
            try:
                plot(Funcion,(x,-20,20), (y,-40,40))
            except:
                print("No es posible gráficar en R2")
    def TresD(tresd) :                           # 3D
        with output2:
            try:
                plot3d(Funcion,(x,-20,20),(y,-40,40), (z,-20,20))
            except:
                print("No es posible gráficar en R3")
    button1.on_click(DosD); button2.on_click(TresD)

    try:
        if Tema ==  'Derivada':
            try:
                def h2( Primera_derivada,Segunda_derivada, Tercera_derivada, Cuarta_derivada, Quinta_derivada):
                    if Primera_derivada == True :
                        try:
                            Primera_derivada = spp.diff(Funcion,x)
                            dom1 = np.arange(-20,20,0.1)
                            ran1 = [Primera_derivada.subs(x,i) for i in dom1]
                            plt.plot(dom1,ran1, 'r', label='Primera derivada')
                            plt.title("Primera derivada"); plt.legend(); plt.grid()
                            print(Primera_derivada)
                        except:
                            pass
                    if Segunda_derivada == True :
                        try:
                            Segunda_derivada = spp.diff(Funcion,x,2)
                            dom2 = np.arange(-20,20,0.1)
                            ran2 = [Segunda_derivada.subs(x,i) for i in dom2]
                            plt.plot(dom2,ran2, 'b', label = "Segunda derivada")
                            plt.title("Segunda derivada"); plt.legend(); plt.grid()
                            print(Segunda_derivada)
                        except:
                            pass
                    if Tercera_derivada == True :
                        try:
                            Tercera_derivada = spp.diff(Funcion,x,3)
                            dom3 = np.arange(-20,20,0.1)
                            ran3 = [Tercera_derivada.subs(x,i) for i in dom3]
                            plt.plot(dom3,ran3, 'g', label = "Tercera derivada")
                            plt.title("Tercera derivada"); plt.legend(); plt.grid()
                            print(Tercera_derivada)
                        except:
                            pass
                    if Cuarta_derivada == True :
                        try:
                            Cuarta_derivada = spp.diff(Funcion,x,4)
                            dom4 = np.arange(-20,20,0.1)
                            ran4 = [Cuarta_derivada.subs(x,i) for i in dom4]
                            plt.plot(dom4,ran4, 'c', label = "Cuarta derivada")
                            plt.title("Cuarta derivada");plt.legend(); plt.grid()
                            print(Cuarta_derivada)
                        except:
                            pass
                    if Quinta_derivada == True :
                        try:
                            Quinta_derivada = spp.diff(Funcion,x,5)
                            dom5 = np.arange(-20,20,0.1)
                            ran5 = [Quinta_derivada.subs(x,i) for i in dom5]
                            plt.plot(dom5,ran5, 'y', label = "Quinta derivada")
                            plt.title("Quinta derivada"); plt.legend(); plt.grid()
                            print(Quinta_derivada)
                        except:
                            pass
                    if Primera_derivada == True and Segunda_derivada == True and Tercera_derivada == True and Cuarta_derivada == True and Quinta_derivada == True :
                        try:
                            plt.plot(dom1, ran1, dom2, ran2, dom3, ran3, dom4, ran4, dom5, ran5)
                            plt.legend(); plt.grid()
                        except:
                            pass
                interact(h2, Primera_derivada = False, Segunda_derivada = False, Tercera_derivada= False, Cuarta_derivada= False, Quinta_derivada= False)
            except:
                pass

        if Tema == 'Límites':
            try:
                def l2(Tendencia):
                    Tendencia = parse_expr(Tendencia)
                    Limite = spp.limit(Funcion, x, Tendencia)
                    print (Limite)         
                interact(l2, Tendencia = '') 
            except:
                pass
        if Tema == 'Raíces de la función':
            try:
                def NR(valor_inicial):
                    valor_inicial = parse_expr(valor_inicial)
                    derivada = spp.diff(Funcion)
                    for i in range(15) :
                        a = spp.sympify(Funcion).subs(x,valor_inicial)                         #Raíces de funciones
                        b = spp.sympify(derivada).subs(x,valor_inicial)
                        valor_inicial = valor_inicial - spp.N(a/b) 
                    return(valor_inicial)
                interact(NR, valor_inicial='') 
            except:
                pass
        if Tema == 'Máximos y mínimos':
            try:
                f = Funcion
                dev1 = spp.diff(f)
                dev2 = spp.diff(dev1)
                enx = spp.solve(dev1, x)
                max_or_min = [dev2.subs(x,i) for i in enx]
                def mamin(max_or_min,enx):
                    try:
                        for i in range(len(max_or_min)):
                            if max_or_min[i] >= 0:                                                #Máximos y Mínimos
                                pos = f.subs(x, enx[i])
                                print((enx[i], pos), "es un mínimo")
                            elif max_or_min[i] < 0:
                                neg = f.subs(x, enx[i])
                                print((enx[i], neg), "es un máximo")
                            else:
                                break
                    except Exception:
                        print("La función tiene soluciones complejas. No es posible determinar máximos o mínimos.")      
                print(mamin(max_or_min,enx))
            except:
                pass
    except:
        pass


def calculo_integral(Tema, Funcion):
    button1, button2 = widgets.Button(description="Dos Dimensiones"), widgets.Button(description="Tres Dimensiones")
    output1, output2 = widgets.Output(), widgets.Output()
    display(button1,output1); display(button2,output2)
    def DosD(dosd) :                            # 2D
        with output1:
            try:
                plot(Funcion,(x,-20,20), (y,-40,40))
            except:
                print("No es posible gráficar en R2")
    def TresD(tresd) :                           # 3D
        with output2:
            try:
                plot3d(Funcion,(x,-20,20),(y,-40,40), (z,-20,20))
            except:
                print("No es posible gráficar en R3")
    button1.on_click(DosD); button2.on_click(TresD)
      
    try:
        if Tema == 'Integrales de una variable':
            try:
                def n(Tipo):
                    if Tipo == 'Indefinida':
                        try:
                            def s(dx, dy):
                                if dx == True:
                                    try:
                                        Integral_indefinida = spp.integrate(parse_expr(Funcion), (x))
                                        dom_1 = np.arange(-20,20,0.1)
                                        ran_1 = [Integral_indefinida.subs(x,i) for i in dom_1]
                                        ran_2 = [parse_expr(Funcion).subs(x,i) for i in dom_1]
                                        plt.plot(dom_1,ran_1, 'r', dom_1, ran_2, 'b', label = Integral_indefinida)
                                        plt.title("Integral indefinida"); plt.legend(); plt.grid()
                                        print(spp.integrate(parse_expr(Funcion), (x)))
                                    except:
                                        pass
                                if dy == True:
                                    try:
                                        print(spp.integrate(parse_expr(Funcion), (y)))
                                    except:
                                        pass
                            interact(s, dx = False, dy = False)
                        except:
                            pass
                    if Tipo == 'Definida':
                        try:
                            def s(a, b, dx, dy):
                                if dx == True:
                                    print(spp.integrate(Funcion, (x, a, b))) 
                                elif dy == True:
                                    print(spp.integrate(Funcion, (y, a, b)))
                                  
                            interact(s, a='', b='', dx = False, dy = False) 
                        except:
                            pass
                interact(n, Tipo = ['Indefinida', 'Definida'])
            except:
                pass
        
        if Tema == 'Sumatoria':
            try:
                def k(a,b):
                    c = 0
                    for i in range(a, b+1):
                        c += parse_expr(Funcion).subs(x, i)
                    return(spp.N(c))
                interact(k, a=widgets.IntText(value=1), b=widgets.IntText(value=1))
            except:
                pass

        if Tema == 'Área bajo una curva':
            try:
                def s(a, b, dx, dy):
                    if dx == True:
                          print(spp.integrate(Funcion, (x, a, b)))
                    if dy == True:
                          print(spp.integrate(Funcion, (x, a, b)))
                interact(s, a='', b='', dx = False, dy = False)
            except:
                pass

        if Tema == 'Volumen bajo una curva':
            try:
                def s(a, b):
                    print(spp.integrate(parse_expr(Funcion)**2, (x, a, b)))
                interact(s, a='', b='')
            except:
                pass

        if Tema == 'Área entre dos curvas':
            try:
                def s(Funcion1, a, b, dx, dy):
                    try:
                        Funcion1 = parse_expr(Funcion1)
                        if dx == True:
                            for i in range(a,b+1):
                                F = Funcion.subs(x,i)
                                F1 = Funcion1.subs(x,i) 
                            if F > F1:
                                c = Funcion - Funcion1
                            if F < F1:
                                c = Funcion1 - Funcion
                                print(spp.integrate(c, (x, a, b)))
                        elif dy == True:
                            for i in range(a,b+1):
                                F = Funcion.subs(y,i)
                                F1 = Funcion1.subs(y,i)
                            if F > F1:
                                c = Funcion - Funcion1
                            if F < F1:
                                c = Funcion1 - Funcion
                            print(spp.integrate(c, (y, a, b)))
                    except Exception:
                        print("No es posible calcular el área.")
                interact(s, Funcion1='', a=widgets.IntText(value=1), b=widgets.IntText(value=1), dx = False, dy = False)
            except:
                pass

        if Tema == 'Volumen entre dos curvas':
            try:
                def s(Funcion1, a, b, dx, dy):
                    try:
                        Funcion1 = parse_expr(Funcion1)
                        if dx == True:
                            for i in range(a,b+1):
                                F = Funcion.subs(x,i)
                                F1 = Funcion1.subs(x,i) 
                            if F > F1:
                                c = Funcion**2 - Funcion1**2
                            if F < F1:
                                c = Funcion1**2 - Funcion**2
                            print(spp.integrate(c, (x, a, b)))
                        elif dy == True:
                            for i in range(a,b+1):
                                F = Funcion.subs(y,i)
                                F1 = Funcion1.subs(y,i)
                            if F > F1:
                                c = Funcion**2 - Funcion1**2
                            if F < F1:
                                c = Funcion1**2 - Funcion**2
                            print(spp.integrate(c, (y, a, b)))
                    except Exception:
                        print("No es posible calcular el volumen.")
                interact(s, Funcion1='', a=widgets.IntText(value=1), b=widgets.IntText(value=1), dx = False, dy = False)
            except:
                pass
    except:
        pass


def calculo_vectorial(Tema, Funcion):
    button1, button2 = widgets.Button(description="Dos Dimensiones"), widgets.Button(description="Tres Dimensiones")
    output1, output2 = widgets.Output(), widgets.Output()
    display(button1,output1); display(button2,output2)
    def DosD(dosd) :                            # 2D
        with output1:
            try:
                plot(Funcion,(x,-20,20), (y,-40,40))
            except:
                print("No es posible gráficar en R2")
    def TresD(tresd) :                           # 3D
        with output2:
            try:
                plot3d(Funcion,(x,-20,20),(y,-40,40), (z,-20,20))
            except:
                print("No es posible gráficar en R3")
    button1.on_click(DosD); button2.on_click(TresD)
      
    try:
        if Tema == 'Derivadas parciales':     # Tema: Derivadas Parciales
            try:                               
                def g(dfx,dfy,dfz) :
                    if dfx == True :
                        try:
                            dfx = spp.diff(Funcion,x)
                            plot3d(dfx,(x,-5,5),(y,-5,5), title='Derivada parcial con respecto a x',xlabel='eje x',ylabel='eje y')
                            print(dfx)
                        except:
                            pass
                    if dfy == True :
                        try:
                            dfy = spp.diff(Funcion,y)
                            plot3d(dfy,(x,-5,5),(y,-5,5), title='Derivada parcial con respecto a y',xlabel='eje x',ylabel='eje y')
                            print(dfy)
                        except:
                            pass
                    if dfz == True :
                        try:
                            dfz = spp.diff(Funcion,z)
                            plot3d(dfz,(z,-5,5),(y,-5,5), title='Derivada parcial con respecto a z',xlabel='eje x',ylabel='eje y') 
                            print(dfz)
                        except:
                            pass
                    if dfx== True and dfy ==True and dfz==True:
                        plot3d(dfx,(x,-5,5),(y,-5,5),(z,-5,5)) and plot3d(dfy,(x,-5,5),(y,-5,5),(z,-5,5)) and plot3d(dfz,(z,-5,5),(y,-5,5),(x,-5,5))       
                    return 
                interact(g, dfx = False, dfy = False, dfz = False)
            except:
                pass
            
        if Tema == 'Integrales Dobles' :                                # Tema: Integrales Dobles   
            try:
                def h(Tipo) :
                    if Tipo == 'Indefinida':                                                 #Indefinida
                        try:
                            intind=spp.integrate(Funcion, (x), (y))
                            print(intind)
                            plot3d(intind, (x,-5,5),(y,-5,5),title='Integral doble indefinida')
                        except:
                              pass
                    if Tipo == 'Definida':                                                # Definida   
                        try:
                            def i(a, b, c,d) :                        
                                print(spp.integrate(Funcion, (x, a, b), (y, c, d)))   
                            interact(i, a='', b='', c='', d='')
                        except:
                            pass
                interact(h,Tipo = ['Indefinida','Definida'])
            except:
                pass
            
        if Tema == 'Integrales Triples' :                                 # Tema: Integrales Triples
            try:
                def h2(Tipo) :                                                         
                    if Tipo == 'Indefinida':                                                # Indefinida
                        try:
                            Indefinida = spp.integrate(Funcion, (x), (y), (z))
                            print(Indefinida)
                        except:
                            pass
                    if Tipo == 'Definida':                                                # Definida   
                        try:
                            def i2(liminf_x, limsup_x, liminf_y, limsup_y, liminf_z, limsup_z) :
                                print(spp.integrate(Funcion, (x, liminf_x, limsup_x), (y, liminf_y, limsup_y), (z, liminf_z, limsup_z)))
                            interact(i2, liminf_x='', limsup_x='', liminf_y='', limsup_y='', liminf_z='', limsup_z='')
                        except:
                            pass
                interact(h2, Tipo = ['Indefinida','Definida']) 
            except:
                pass 
    except:
        pass


tab_contents = ['Pre-Álgebra','Álgebra lineal', 'Cálculo diferencial', 'Cálculo integral','Cálculo vectorial']
funcion=[interactive(pre_algebra, Tema = ['Operaciones Básicas','Factores y Números primos','Logaritmos, Radicales y Exponenciales'], Funcion=widgets.Text(description="Función: ", value="")),
         interactive(algebra_lineal, Tema = ['Operaciones entre matrices','Operaciones entre vectores','Sistema de ecuaciones lineales']),
         interactive(calculo_diferencial, Tema = ['Derivada', 'Límites', 'Raíces de la función', 'Máximos y mínimos'], Funcion=widgets.Text(description="Función: ", value="")),
         interactive(calculo_integral, Tema = ['Integrales de una variable','Sumatoria', 'Área bajo una curva', 'Volumen bajo una curva', 'Área entre dos curvas', 'Volumen entre dos curvas'], Funcion=widgets.Text(description="Función: ", value="")),
         interactive(calculo_vectorial, Tema = ['Derivadas parciales','Integrales Dobles', 'Integrales Triples'], Funcion=widgets.Text(description="Función: ", value=""))]

tab = widgets.Tab()
tab.children = [widgets.VBox(children = i.children) for i in funcion]
for i in range(len(tab_contents)):
    tab.set_title(i,tab_contents[i])
display(tab)


# In[ ]:




