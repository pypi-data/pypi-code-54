import pandas as pd
import difflib as df
from fuzzywuzzy import fuzz
from cleanco import cleanco
import numpy as np





def merge_files(df,df1,vendor_name_column,actual_name_column):
    try:
        merged=pd.merge(df,df1,how='left',left_on=vendor_name_column,right_on=actual_name_column,indicator=True)
        merged_leftout=merged[merged['_merge'].isin(['left_only'])].dropna(how='all')
        merged_leftout=merged_leftout.drop_duplicates()
        merged_leftout= merged_leftout.drop('_merge',axis=1)
        merged_leftout=merged_leftout.dropna(subset=[vendor_name_column])
        merged_leftout=merged_leftout.drop_duplicates(subset=vendor_name_column)

        return merged_leftout
    
    except Exception as e:
        print(type(e),e)

    




def vendor_name_match(vendor_names_file_path, actual_vendor_names_file_path,special_cases,actual_name_column,vendor_name_column,replace=False):
    """
       Matches the partial vendor names to the actual vendor names

       paramerters
       =============
       - vendor_names_file_path : path of excel/csv file name for which vendor name to be matched
       - actual_vendor_names_file_path : path of excel/csv file name containing actual vendor name
       - actual_name_column: column name of the file containing actual vendor name
       - vendor_name_column: column name of the file containing vendor name to be matched
       - replace : True if vendor name are to be replaced with actual vendor names

       Returns
       ===========
       dataframe 

    """
    
    index_to_be_removed=[]

    if vendor_names_file_path.endswith('.xlsx'):
        try:
            data=pd.read_excel(vendor_names_file_path)
        except Exception as e:
            print(type(e),e)
            
    elif vendor_names_file_path.endswith('.csv'):
        try:
            data=pd.read_csv(vendor_names_file_path)
        except Exception as e:
            print(type(e),e)
    else:
        raise TypeError('File to be matched should be either .xlsx or .csv format')

    
    if actual_vendor_names_file_path.endswith('.xlsx'):
        try:
            actuals = pd.read_excel(actual_vendor_names_file_path,usecols=[actual_name_column])
        except Exception as e:
            print(type(e),e)
    elif actual_vendor_names_file_path.endswith('.csv'):
        try:
            actuals = pd.read_csv(actual_vendor_names_file_path,usecols=[actual_name_column])
        except Exception as e:
            print(type(e),e)
    else:
        raise TypeError('File containing actual venodor name should be either .xlsx or .csv format')
    
        
    try:
        merged_leftout=merge_files(data,actuals,vendor_name_column,actual_name_column)

        merged_leftout[vendor_name_column]=merged_leftout[vendor_name_column].str.strip()
        merged_leftout[vendor_name_column]=' '+merged_leftout[vendor_name_column]+' '
        actuals[actual_name_column]=actuals[actual_name_column].str.strip()
        actuals[actual_name_column]=' '+actuals[actual_name_column]+' '

        for index in merged_leftout[vendor_name_column].index:
            try:
                ind=actuals[actuals[actual_name_column].str.contains(merged_leftout[vendor_name_column][index].replace(',','').replace('\'','').replace('.','').replace('&',' '),case=False)].index
            except:
                ind=actuals[actuals[actual_name_column].str.contains(merged_leftout[vendor_name_column][index].replace(',','').replace('\'','').replace('.','').replace('&',' ')+')',case=False)].index
            if special_cases[0] in merged_leftout[vendor_name_column][index].lower().replace('-','').replace(' ','') or special_cases[1] in merged_leftout[vendor_name_column][index].lower().replace('-',''):
                ind=actuals[actuals[actual_name_column].str.contains(cleanco(merged_leftout[vendor_name_column][index].replace(',','').replace('\'','').replace('.','').replace('&',' ')).clean_name(),case=False)].index

            if len(set(actuals[actual_name_column][ind].str.replace(',','').replace('.','').str.lower()))== 1:
                merged_leftout[actual_name_column][index]=actuals[actual_name_column][ind[0]]
                index_to_be_removed.append(index)
            elif len(set(actuals[actual_name_column][ind].str.replace(',','').replace('.','').str.lower()))> 1:
                index_to_be_removed.append(index)           

        index_missed=merged_leftout.drop(index_to_be_removed,axis=0).index
    except Exception as e:
        print(type(e),e)
        
    try:
        actuals_lower=list(actuals[actual_name_column].str.lower())
        del actuals
        del index_to_be_removed
        for index in index_missed:
            closest_strings=df.get_close_matches(merged_leftout[vendor_name_column][index].lower(),actuals_lower,cutoff=0.5,n=4)
            ratio=[]
            for string in closest_strings:

                ratio.append(fuzz.partial_ratio(" "+cleanco(cleanco(merged_leftout[vendor_name_column][index].lower().replace(' cda ',' canada ').replace(' intn ',' international ').replace(' int\'l ',' international ').replace(' intl ',' international ').replace(' ind. ',' industries ').replace(' ind ',' industries ').replace(' prds ',' products ').replace(' pro ',' products ').replace('(','').replace(')','').replace('.','').replace(',','').replace('&','and')).clean_name()).clean_name()+' ',' '+cleanco(cleanco(string.lower().replace(' ind. ',' industries ').replace(' intn ',' international ').replace(' ind ',' industries ').replace(' int\'l ',' international ').replace(' intl ',' international ').replace(' prds ',' products ').replace(' cda ',' canada ').replace(' pro ',' products ').replace('.','').replace(',','').replace('&','and').replace('(','').replace(')','')).clean_name()).clean_name()+' '))
            if len(ratio)!=0 and ratio[np.argmax(ratio)] > 95 : #if not argmx, it will take first >95 value
                merged_leftout[actual_name_column][index]=closest_strings[np.argmax(ratio)].upper()
                actuals_lower.remove(closest_strings[np.argmax(ratio)])

        merged_leftout[vendor_name_column]=merged_leftout[vendor_name_column].str.strip()
        merged_leftout[actual_name_column]=merged_leftout[actual_name_column].str.strip()
        if replace:
            merged_leftout[vendor_name_column][~merged_leftout[actual_name_column].isnull()]=merged_leftout[actual_name_column][~merged_leftout[actual_name_column].isnull()]
            merged_leftout=merged_leftout.drop(actual_name_column,axis=1)
        return merged_leftout
    except Exception as e:
        print(type(e),e)
    
    