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

import matplotlib.pyplot as plt
from simublocks.dialog import Dialog

class Plot:

    def run(s):
        count = 0
        for i in s['graphs']:
            count += 1
            Plot.figure(count, i, {**s['systems'], **s['inputs'], **s['functions'], **s['sums']}, s['t'])

        #Plot.plotInput(s['inputs'], s['t'])
        #Plot.plotSystem(s['systems'], s['t'])
        plt.show()
    
    
    def figure(count, graph, blocks, t):
        plt.figure(count)
        legend = []
        for line in graph.code:
            if line['check']:
                if line['type'] in ['input', 'system', 'function', 'sum']:
                    try:
                        block = next(filter(lambda i: blocks[i].name == line['name'], blocks))
                        block = blocks[block]
                    except Exception as e: 
                        Dialog.alert("Alert", [
                            "Error in the 'graph' block", 
                            "Please, after removing or creating a new 'system' or 'input' block, remove and recreate all 'graph' blocks"
                        ])
                    legend.append(line['legend'])
                if line['type'] == 'input':
                    plt.plot(t[:-1], block.input[:-1],line['color'])
                elif line['type'] in ['function','system','sum']:
                    plt.plot(t[:-1], block.y[:-1],line['color'])
        plt.legend(legend)
        plt.grid()