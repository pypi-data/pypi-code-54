import pandas as pd
import numpy as np
import os

        
def ispump(pp):
    '''is pump is used to check whether the input is a pump'''

    try:
        df=pp.go()
    except:
        return False
    if not isinstance(df, pd.DataFrame): return False
    if df.shape[0]==0: return False
    
    return True

def demo():
    '''demo is used to demonstrate the whole clubear class'''
    
    mylist=['manager','pump','check','plot','model','tank']
    mylist=sorted(mylist)
    
    greeting='''
Welcome to CluBear!

This is a package designed for *Interactive* statistical analysis for massive 
datasets. The key idea used here is subsampling. The package is developed by 
CluBear Research Group. You are welcome to visit our official website at 
www.xiong99.com.cn. You are also welcome to follow us at our official WeChat 
account (ID: CluBear). Enjoy!
'''
    print(greeting)
    print('\n',mylist,'\n')
    
    return
