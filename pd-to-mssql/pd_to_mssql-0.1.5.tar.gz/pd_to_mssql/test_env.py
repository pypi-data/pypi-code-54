import pandas as pd
import pyodbc
from pd_to_mssql import to_sql

cnxn_str = 'Driver={ODBC Driver 17 for SQL Server};Server=oh01msvsp64.workflowone.net\proddas1;Database=DataScience;Trusted_Connection=yes;'

df = pd.read_csv('test.csv', encoding='latin')

for col in df.columns:
    if col[-1] == ' ':
        df.rename(columns={col: col.strip()}, inplace=True)

for col in ['PL Sales Price', 'PL Sales', 'PL Cost', 'Sales Tax', 'Discount Amt']:
    df[col] = df[col].apply(lambda x: float(str(x).replace(',', '')))

to_sql(df, 'test', cnxn_str, index=False, replace=True)
