from rohan.global_imports import *
from rohan.dandage.io_dict import read_dict,to_dict

def get01_dpeaks_raw(date2dpeakp,dpeaks_rawp):
    date2dpeakp=read_dict(date2dpeakp)
    df1=pd.concat({k: read_table(date2dpeakp[k]) for k in date2dpeakp},names=['date'],axis=0).reset_index()
    to_table(df1,dpeaks_rawp)
        
def get02_dstats(dpeaks_rawp,dstatsp):
    df01=read_table(dpeaks_rawp)
    df1=df01.groupby(['date','rally #']).agg({
                                          'time (ms)':[len,np.mean,lambda x: np.max(x)-np.min(x)],
                                          'db (log-scale) mean':[np.mean],
                                          })
    df1.columns=coltuples2str(df1.columns)
    df1=df1.reset_index()
    rename=dict(zip(['date',
     'rally #',
     'time (ms) len',
     'time (ms) mean',
     'time (ms) <lambda_0>',
     'db (log-scale) mean mean'],
     ['date',
     'rally #',
     'bounces all',
     'time (ms) mean',
     'rally duration',
     'loudness (db)']))
    df2=df1.rename(columns=rename)
    df2['shots']=df2['bounces all']/2
    df2['rally count']=df2['shots']/2
    df2['rally speed']=df2['rally count']/df2['rally duration']
    df2['rally speed']=df2['rally speed'].replace([np.inf,-np.inf],np.nan)
    df2['date']=df2['date'].apply(int)
    to_table(df2,dstatsp)
    
def get03_plot_stats(cfg,dstatsp):
    from ppong.plots import plot_stats
    from rohan.dandage.io_strs import get_datetime
    outp=f'plot/scatters_stats {get_datetime()}.png'
    plot_stats(read_table(dstatsp))
    savefig(outp)