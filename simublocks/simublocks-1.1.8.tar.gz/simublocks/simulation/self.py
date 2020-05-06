# MIT License
#
# Copyright (c) 2020 Anderson Vitor Bento
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
from simublocks.element import Workspace
from simublocks.simulation.tools import simulationTools
from simublocks.simulation.plot import Plot
from simublocks.dialog import Dialog

class Self(simulationTools):

    def __init__(self,T,tf):
        conns = Workspace.connections
        blocks = Workspace.blocks
        s = {
            't': np.arange(0,tf+T,T),
            'T': T,
            'inputs': {},
            'systems': {},
            'functions': {},
            'sums': {}
        }

        try:
            exec(Workspace.importCode,s)
        except Exception as e: 
            print(e)
            Dialog.alert("Alert", [
                "Error importing your code",
                str(e)
            ])

        s = self.loadBlocks(s)
        s['graphs'] = Workspace.graphs
        
        for i in s['inputs']:

            try:
                exec(s['inputs'][i].code,s)
            except Exception as e: 
                print(e)
                Dialog.alert("Alert", [
                    "Error in the input block '" + s['inputs'][i].name + "'",
                    str(e)
                ])
                
            for k in range(len(s['t'])):
                try:
                    s['inputs'][i].input[k] = s[s['inputs'][i].name](s['t'][k],k)
                except Exception as e: 
                    print(e)
                    Dialog.alert("Alert", [
                        "Error in the input block '" + s['inputs'][i].name + "'", 
                        "Remember that the function and the block must have the same name"
                    ])

        for i in s['functions']:
            try:
                func = s['functions'][i]
                exec(func.code,s)
                s['functions'][i].func = s[func.name]
            except Exception as e: 
                print(e)
                Dialog.alert("Alert", [
                    "Error in the function block '" + s['inputs'][i].name + "'",
                    str(e)
                ])
        
        # Simulation

        for k in range(len(s['t']) -1):
            
            for i in s['systems']:
                b = s['systems'][i]
                
                if 'otherblock' in b.conn[0]:
                    first = b.conn[0]['otherblock']
                    _input = self.search(first, k)
                else:
                    _input = 0
                b.x[k+1] = b.ss[0]@b.x[k] + b.ss[1]*_input
                b.y[k] = b.ss[2]@b.x[k] + b.ss[3]*_input

            for i in s['functions']:
                b = s['functions'][i]
                if np.isnan(b.y[k]):
                    if 'otherblock' in b.conn[0]:
                        first = b.conn[0]['otherblock']
                        _input = self.search(first, k)
                    else:
                        _input = 0
                    b.y[k] = b.func(_input)

            for i in s['sums']:
                b = s['sums'][i]
                if np.isnan(b.y[k]):
                    soma = 0
                    if 'otherblock' in b.conn[0]:
                        next0 = b.conn[0]['otherblock']
                        if b.code[0] == "+":  soma += self.search(next0, k)
                        else:  soma-= self.search(next0, k)
                    
                    if 'otherblock' in b.conn[2]:
                        next2 = b.conn[2]['otherblock']
                        if b.code[1] == "+": soma += self.search(next2, k)
                        else: soma-= self.search(next2, k)

                    b.y[k] = soma
                
        Plot.run(s)
        