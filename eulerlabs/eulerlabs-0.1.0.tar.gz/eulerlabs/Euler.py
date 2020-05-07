'''
Created on October 6, 2015
@author: Anil P Singh
@email : SINGH.AP79@GMAIL.COM  
'''
import os
import sys
import sqlite3
import traceback
import time
import datetime
import math
import numpy as np
import shlex

#@# GLOBAL Definitions
llog = None
sqllog = None

#@# GENERAL Utilities
def replace_all (string,seq,repl):
    while seq in string:
        string = string.replace(seq,repl)
    return string


def replace_many(string,seqL,replL):
    for seq,rep in zip(seqL,replL):
        string = string.replace(seq,rep)
    return string
    
def print_error(err,place=''):
    '''
    A utility function for better diagnostic reporting.
    '''
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback, limit=5, file=sys.stdout)
    p = sys._getframe(1).f_code.co_name
    if place == '' : place = p
    sys.stderr.write(('ERROR ('+place+'):  %s\n') % str(err))
    
    
def clean_text(text, splitChar=','):
    '''
     1. remove unicode sentinetls u'xxx'
     2. remove (, ) characters 
     3. remove (\\) characters
     4. under development
     '''
    text = text.strip()
    ##Getting rid of unicode sentinel
    text = text.replace('u\'','')
    ##Following Characters mess-up with SQL
    text = text.replace('\'','')
    text = text.replace('(','')
    text = text.replace(')','')
    text = text.replace('.','')
    text = text.replace(' ','')
    text = text.replace('%','')
    text = text.replace('-','')
    ##print "clean_text",text
    return text, text.split(splitChar)


def sqlite_table_info(tableName):
    return "PRAGMA table_info(?tableName?)".replace("?tableName?",tableName)


def create_table_qry(tabName, varDict={}, uniqueIdFlag=False,uIdName='PYDAN_ROW_NUM'):
    try:
        query = ' CREATE  TABLE '+tabName+''' ( \n'''
        if(uniqueIdFlag == True):
            query = query + uIdName+'        VARCHAR,\n '
        varterms = []
        for varname in varDict:
            vartype = varDict[varname]            
            varterms.append('       '.join([varname,vartype]))
        query = query+ ',\n '.join(varterms)
        query = query+'\n )'
        return query
    except Exception as err:
        print_error(err, 'euler.create_table_qry')        
        

def clean_string(text,replaceHyphen=True):
    try:
        text = text.strip()
        ##Getting rid of unicode sentinel
        text = text.replace('u\'','')
        ##Following Characters mess-up with SQL
        text = text.replace('\'','')
        text = text.replace('(','')
        text = text.replace(')','')
        text = text.replace('.','')
        ##text = text.replace(' ','')
        text = text.replace('%','')
        if(replaceHyphen==True):
            text = text.replace('-','')
        text =text.replace('"','')
        ##print "clean_text",text
        ##Removing all non-ascii characters.
        text = ''.join([i for i in text if ord(i)<128])
        return text
    except Exception as err:
        print_error(err, 'euler.clean_string') 

#@# SQL Utili
def connection(url):
    '''
    Provides a connection object to sqlite.
    Registers some missing functions to sqlite.
    '''
    try:
        conn = sqlite3.connect(url)
        conn.create_function('log',func=math.log,narg=1)
        conn.create_function('alog',func=math.exp,narg=1)
        conn.create_function('sqrt',func=math.sqrt,narg=1)
        conn.create_function('pow',func=math.pow,narg=2)
        return conn
    except Exception as err:
        print_error(err,'euler.connection')

def attach_dbase(conn, name,obase):
    conn.execute("ATTACH '"+obase+"' AS "+name+';')
    conn.commit()
    
def get_bysql(query,conn,verbose=False):
    'Returns list of lists data fetched by query rowXcolumns format'
    try:
        #query = query.replace('?srcName?',tabName)
        if verbose==True : print (query)
        results = conn.cursor().execute(query)
        dataSet = []
        for r in results:
            rList = list(r)
            dataSet.append(rList)
        return dataSet  
    except Exception as err:
        
        print ("\n\n****Exception Encountered****\n")
        print ('Not Happy With \n'+query)
        print_error(err,'euler.get_bysql')
        
def run(query,conn,mute=False,nice_print=False, verbose=False):
    'Returns list of lists data fetched by query rowXcolumns format'
    if mute == True : return
    try:
        #query = query.replace('?srcName?',tabName)
        if verbose==True : print (query)
        results = conn.cursor().execute(query)
        
        if results == None: return 
        if results.description == None : return
        columns = [d[0] for d in results.description]
        columns = ','.join(columns)
        print ('='*len(columns))
        print(columns)
        print ('='*len(columns))
        dataSet = []
        for r in results:
            rList = [str(ri) for ri in list(r)]
            print (','.join(rList))
        print ('='*len(columns)+'\n')
        return dataSet  
    except Exception as err:
        
        print ("\n\n****Exception Encountered****\n")
        print ('Not Happy With \n'+query)
        print_error(err,'Euler.run')


"""
def print_logo():
    logo='''
    ************************************************
    *                    EULER                     *
    *    A SQLITE POWERED DATA SCIENCE TOOLKIT     *
    *          SINGH.AP79@GMAIL.NOSPAM.COM         * 
    *                                              * 
    ************************************************
    '''
    logo = '\n'.join([l.strip() for l in logo.split('\n')])
    print (logo)
#print_logo()
"""

def download_csv_bysql(query,conn,write_to,verbose=False):
    'Returns list of lists data fetched by query rowXcolumns format'
    try:
        #query = query.replace('?srcName?',tabName)
        if verbose==True : print (query)
        write_to  = open(write_to,'w')
        query = query.replace(';','')
        results = conn.cursor().execute(query)
        columns = [d[0] for d in results.description]
        write_to.write(','.join(columns)+'\n')
        counter = 0
        for r in results:
            if (counter-1)%10000 == 0: print ('Downloaded :',counter,' records.')
            rList = [str(ri) for ri in list(r)]
            rList = ','.join(rList)+'\n'
            write_to.write(rList)
            counter = counter+1
            
        write_to.close()    
    except Exception as err:
        print ("\n\n****Exception Encountered****\n")
        print ('Not Happy With \n'+query)
        print_error(err,'euler.download_csv_bysql')
        
        
def get_ncols_bysql(query,n,conn,verbose=False,col_keys=None):
    'Returns list of lists data fetched by query in columnXrow format'
    try:
        if n==1 : return get_1col_bysql(query, conn)
        res = get_bysql(query,conn,verbose=verbose)
       
        if len(res) == 0: 
            res = [[]]*n
           
            return res 
        data_cols = []
        for i in range(0,n):    
            data_cols.append([line[i] for line in res])
        if col_keys == None:
            return tuple(data_cols)
        else: return dict(zip(col_keys,data_cols))
    except Exception as err:
        print_error(err,'euler.get_ncols_bysql')
        
 
def get_1col_bysql(query,conn):
    try:
        'Return list data fetched by query for a single output'
        res = get_bysql(query, conn)
        col1 = [line[0] for line in res]
        return col1
    except Exception as err:
        print_error(err,'euler.get_1col_bysql')



def execute(script,conn,verbose=1):
    try:
        cursor = conn.cursor()
        for sql in script.split(';'):
            if sql.strip() == "":
                pass
            else:       
                try:
                    if (llog != None): llog.write_log(sql)
                    if verbose > 0: print (sql)
                    cursor.execute(sql)
                    conn.commit()
                except Exception as err:
                    print_error(err,'euler.execute')
                    print ('''
                    Not happy with       
                    '''+sql)
                    if 'DROP ' not in sql: sys.exit(-9999)
                    
        return 0
    except Exception as err:
        print_error(err,'Euler.execute')

def mv_db1_db2(conn,name,tabName):
    sql = ''' 
    CREATE TABLE ?name?.?tabName? as SELECT * FROM ?tabName? t2;
    '''
    sql = sql.replace('?name?',name)
    sql = sql.replace('?tabName?',tabName)
    execute(sql,conn,verbose=1)
    conn.commit()
    
"""
keep working...
""" 
def print_data_dict(data_dict,order=''):
    order = order.split(',')
    if len(order)==0:
        order = data_dict.keys()
    data_array = []
    for k in order:
        data_array.append(data_dict[k])
    print (', '.join(order))
    
    rows = 0.0
    cols = len(data_array)
    if cols > 0: rows = len(data_array[0])
    
    for row in range(0,rows):
        pass

# This section needs a lot of work.
#@# CSV To Sqlite: 
class pycsv_reader:
    '''
     csv reader
    '''
   
    def __init__(self,fName,headers=[],separator = ',',firstLineIsHeader=True, 
                 reNames={}):
        self.pFirstLineIsHeader = firstLineIsHeader
        self.pSeparator = separator
        self.pFname = fName
        if len(headers) !=0 and firstLineIsHeader==True:
            raise RuntimeError('Ambiguous Header Specifications')
        if os.path.exists(self.pFname):
            self.pFile = open(self.pFname,'r')
            #firstLine   = self.pFile.readline().split(self.pSeparator)
            headLine = self.pFile.readline()
            for key in reNames.keys():
                headLine=headLine.replace(key,reNames[key])
            firstLine = headLine.strip().split(self.pSeparator)
            firstLine = [word.strip() for word in firstLine]
            
            #print firstLine
            if len(headers) == 0 and firstLineIsHeader==False:
                numCol = len(firstLine)
                for n in range (1,numCol):
                    self.pHeader.append(str(n))
            elif len(headers) == 0 and firstLineIsHeader==True:
                self.pHeader = firstLine
            elif len(headers) != 0 and firstLineIsHeader==False:
                #if len(firstLine) == len(headers):
                self.pHeader = headers
                #else:
                #    raise RuntimeError("Not implemented yet")
            self.pHeader = map (str.strip, self.pHeader)
            self.pHeader = map (clean_string,self.pHeader)
            ##The clean_text return two values: Check how it works here.
            ## Not easy to use map so let us replace things by list comprehension 
            ##self.pHeader = map (clean_text.,self.pHeader)
            ##@ANIL I don't want it this ugly
            tempHeader = []
            for cname in self.pHeader:
                a, h = clean_text(cname,self.pSeparator)
                a = a.replace('"','')
                tempHeader.append(a)
            self.pHeader = tempHeader
        elif IOError:
            print ("Unable to find file: "+str(fName))
    
    def __del__(self):
        '''
        Returning the resources.
        '''
        self.pFirstLineIsHeader = None
        self.pSeparator = None
        self.pFname = None
        self.pHeader = None
        self.close()
        self.pFile = None
        
    def close(self):
        try:
            self.pFile.close()            
        except Exception as err:
            sys.stderr.write('ERROR: %s\n' % str(err))


            
    def toStr(self):
        print (self.pFname)
        for col in self.pHeader:
            print (col)   
         
   
    
    def  to_database(self,tabName,database,varNames=[],varTypes=None,ur=False, 
                     replaceList=[],useshlex=False,nestedcommareplace=None,
                     reportEvery = 10000,
                     verbose = False,
                     conn = None
                     ):
        '''writes the csv file to a table.
           ---returns a pydset object associated with table
        '''
          
        
        try:
            pConn = conn
            if pConn == None:
                pConn = sqlite3.connect(database)
            print ('drop table if exists '+tabName)
            pConn.execute('drop table if exists '+tabName)
            print ('Here!')
            pConn.commit()
            if len(varNames)==0:
                varNames = self.pHeader
            if varTypes == None:
                varTypes = {}
                
            for var in varNames:
                #print var
                if var not in varTypes: varTypes[var]='VARCHAR'
                else: varTypes[var]=varTypes[var].strip()


            query = create_table_qry(tabName,varDict=varTypes
                                            ,uniqueIdFlag=False
                                           )
            
            if verbose == True: print (query)
            pConn.execute(query)
            print ("Done")
            pConn.commit()
            
            manyLines = []
            q = ['?']*len(varNames)
            qr = '('+','.join(q)+')'
            query = 'insert into '+tabName+'('+','.join(varNames)+') values '+qr
            
            #print (query)
            pConn.execute('PRAGMA synchronous=OFF');
            counter = 0;            
            for row in self.pFile:
                if (counter%int(reportEvery) == 0):
                    print ("Lines Read: ",counter)
                row = row.strip()
                if row == '': continue
                line = None
                if useshlex==True:
                    if nestedcommareplace == None:
                        #rasieException
                        print_error('pydata.shlex.screwup')
                        return
                    
                    row = row.replace(",,",",'',")
                    splitter = shlex.shlex(row, posix=True)
                    splitter.whitespace=','
                    splitter.whitespace_split = True
                    line = list(splitter)
                    line = [l.replace(',',nestedcommareplace) for l in line]
                    #print ('shlex'+'-'.join(line))
                else: line = row.split(self.pSeparator)
                if len(line)==0: continue
                  
                else:
                    for replacement in replaceList:
                        key = replacement.strip().split(":")[0]
                        val = replacement.strip().split(":")[1]
                        line =  [t.replace(key,val) for t in line]
                        
                    line = [l.replace("\xa0", " ") for l in line]
                    
                    manyLines.append(tuple(line))
                    #print (line)
                    if (counter%1)==0:
                        if counter == 0:
                            pass
                        else:
                            if verbose ==  True: print (query,manyLines)
                            pConn.cursor().executemany(query,manyLines)
                            
                            manyLines =[]
                    #if(select):
                    counter = counter+1
                
            if len(manyLines)>0:
                pConn.executemany(query,manyLines)
            else: self.pFile.close()
            ##Move the cursor back to top of the csv file.
            pConn.commit()
                    
        except Exception as err:
                print_error(err,"pycsv_reader.to_database")
            
    def reader(self, numLines=-9999):
        rows = []
        nLines = 0
        for row in self.pFile:
            r,rowList = clean_text(row, self.pSeparator)
            rows.append(rowList)
            nLines = nLines+1
            if(numLines != -9999 and nLines>=numLines):
                break
        self.pFile.seek(0,0)
        if (self.pFirstLineIsHeader == True):
            self.pFile.readline()
        return rows
    
    def dict_reader(self,numLines):
        data = self.reader(numLines)
        dataDict = []
        for row in data:
            ##Row is a list of variables.
            ##We zip it to headers to form a dictionary.
            dictRow = dict(zip(self.pHeader,row))
            dataDict.append(dictRow)
        return dataDict




def csvToSqlite(csvfile,sqlitefile,tabName):
    try:
        csv = pycsv_reader(csvfile)
        csv.to_database(tabName,database=sqlitefile)        
        csv.close()
    except Exception as err:
        print_error(err)
        

def list2D_tosqlite(headerList1D,dataList2D,tabName,dbFile,tempFile):
    try:
        """
        Note: This is to be changed. It should rather use 
        dict_tosqlite.
        """
        file = open(tempFile,'w')
        file.write(','.join(headerList1D)+'\n')
        for week in dataList2D:
            week = [str(w) for w in week]
            file.write(','.join(week)+'\n')
        file.close()
        csvToSqlite(tempFile,dbFile,tabName)
        
        ##Cleanup the temporary file.
        if os.path.exists(tempFile):
            os.remove(tempFile)

    except Exception as err:
        print_error(err)
   
def dict_tosqlite(headcolDict,tabName,conn):
    try:
        columns = headcolDict.keys()
        if len(columns) == 0:
            raise Exception ('''Exception: No Valid Column Names Found.''')
        
        column_type = [ isinstance(col,str)  for col in columns]
        if not (all(column_type)) :
            raise Exception ('''Exception: Non string value specified for headers''')

        #Sanity Checks on data.
        number_of_rows = []
        for column in columns:
            number_of_rows.append(len(headcolDict[column]))
            
        if sum(number_of_rows) != number_of_rows[0]*len(number_of_rows):
            raise Exception ('''Exception: All Columns must have same number of rows. ''')

        sql = '''
        drop table if exists ?tabName?;
        CREATE TABLE ?tabName? (
        ?vardefs?
        );
        '''
        sql = sql.replace('?tabName?',tabName)
        vardefs = []
        for vvar in columns:
            vardefs.append('?vvar? TEXT'.replace('?vvar?',vvar))
        vardefs = ','.join(vardefs)
        sql = sql.replace('?vardefs?',vardefs)
        
        ## Insert the data into the table.
        insrt = 'INSERT INTO ?tabName? (?cols?) values (?vals?)'
        insrt = insrt.replace('?tabName?',tabName)
        cols  = ', '.join(columns)
        insrt = insrt.replace('?cols?',cols)
        data_cols = [headcolDict[col] for col in columns]
        data_rows = list(map(list, zip(*data_cols))) #transpose cols to rows.
        inserts = []
        for row in data_rows:
            row = ', '.join(["'"+str(dat)+"'" for dat in row])
            inserts.append(insrt.replace('?vals?',row))
        
        #print (inserts)
        sql = sql+';\n'.join(inserts)
        sql = replace_all(sql,'  ',' ')
        execute(script=sql,conn=conn,verbose=0)
    except Exception as err:
        print_error(err,'euler.dict_tosqlite')
        
 

#@# LOGGING System
##Open a logging system.
class logcabin:
    def __init__(self):
        logbook = None
        start_time = None
        start_time_string = None
    
    def open_log(self,fname):
        self.start_time = time.time()
        self.logbook = open(fname,'w')
        self.start_time_string =  datetime.datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S')
        self.logbook.write("--Starting Execution at: "+self.start_time_string+"\n")

    def close_log(self):
        end_time = time.time()
        end_time_string =  datetime.datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
        print (self.start_time_string, end_time_string)
        if self.logbook != None and self.start_time != None:
            #tdiff = datetime.datetime.fromtimestamp(end_time-self.start_time).strftime('%H:%M:%S')
            self.logbook.write("\n--Start Time: "+self.start_time_string+", End Time: "+end_time_string+"\n\n")
            self.logbook.write("---Total Duration of Run: ?")
            self.logbook.write("\n\n---++++End Of Execution+++++\n\n")
            self.logbook.close()

    def write_log(self,msg):
        msg = "\n--++++++++++++++++++++++++++++++++++++++++\n"+msg+"\n"
        self.logbook.write(msg)
