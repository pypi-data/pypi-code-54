

import pandas as pd
class Csv2Xml:
    #Initialize the file path,root node,child node
    def __init__(self,CsvFilePath,root='Payload',children='tuple'):
        self.CsvFilePath=CsvFilePath
        self.df=pd.read_csv(self.CsvFilePath)
        self.root=root
        self.children=children
    #Column Value
    def __getColumn(self):
        s='<'+self.children+'>\n'
        for i in self.df.columns:
            s+='<'+i+'>%s<'+i+'/>\n'
        s+='</'+self.children+'>'
        return s  
    def __helper(self,row):
        s=self.__getColumn()
        res=[]
        for i,col in enumerate(self.df.columns):
            if(i==len(row)-1):
                res.append(row[i])
            else:
                res.append(row[i])
        return s % tuple(res)
    def parse2Xml(self):
        s='<'+self.root+'>\n'
        s+='\n'.join(self.df.apply(self.__helper,axis=1))
        s+='</'+self.root+'>'
        return s
